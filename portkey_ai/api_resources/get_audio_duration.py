import wave
import os


def get_audio_file_duration(file_path):
    """
    Calculate the duration of an audio file in milliseconds.
    Supports: flac, mp3, mp4, mpga, m4a, ogg, wav

    Args:
        file_path (str): Path to the audio file

    Returns:
        str: Duration in milliseconds as a string
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    file_size = os.path.getsize(file_path)

    # WAV files - use wave module
    if file_ext == ".wav":
        with wave.open(file_path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return str(int(duration * 1000))

    # MP3 files
    elif file_ext in [".mp3", ".mpga"]:
        with open(file_path, "rb") as f:
            # Check for ID3v2 tag
            header = f.read(10)
            offset = 0
            id3v2_size = 0

            if header[:3] == b"ID3":
                # Calculate ID3v2 tag size
                tag_size = (
                    ((header[6] & 0x7F) << 21)
                    | ((header[7] & 0x7F) << 14)
                    | ((header[8] & 0x7F) << 7)
                    | (header[9] & 0x7F)
                )
                offset = tag_size + 10
                id3v2_size = offset
                f.seek(offset)
            else:
                f.seek(0)  # Reset to beginning if no ID3v2 tag

            # Find first valid MPEG frame by reading small chunks
            chunk_size = 4096
            frame_header = None
            chunk_offset = 0

            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Look for frame sync pattern in this chunk
                for i in range(len(chunk) - 3):
                    if chunk[i] == 0xFF and (chunk[i + 1] & 0xE0) == 0xE0:
                        frame_header = chunk[i : i + 4]
                        offset += i
                        break

                if frame_header:
                    break

                offset += len(chunk)
                chunk_offset += 1

                # Seek back 3 bytes to handle case where sync is split between chunks
                if chunk and len(chunk) >= 3:
                    f.seek(-3, 1)
                    offset -= 3

            if not frame_header:
                return None  # No valid MPEG frame found

            # Extract version, layer, bitrate index, sample rate index
            version_bits = (frame_header[1] & 0x18) >> 3
            layer_bits = (frame_header[1] & 0x06) >> 1
            bitrate_index = (frame_header[2] & 0xF0) >> 4
            sample_rate_index = (frame_header[2] & 0x0C) >> 2

            # Determine MPEG version (2.5, 2, 1)
            if version_bits == 0:
                version = 2.5
            elif version_bits == 2:
                version = 2
            elif version_bits == 3:
                version = 1
            else:
                return None  # Invalid version

            # Determine layer (1, 2, 3)
            if layer_bits == 1:
                layer = 3
            elif layer_bits == 2:
                layer = 2
            elif layer_bits == 3:
                layer = 1
            else:
                return None  # Invalid layer

            # Lookup tables for bitrates
            bitrate_table = {
                1: {  # MPEG 1
                    1: [
                        0,
                        32,
                        64,
                        96,
                        128,
                        160,
                        192,
                        224,
                        256,
                        288,
                        320,
                        352,
                        384,
                        416,
                        448,
                        0,
                    ],  # Layer 1
                    2: [
                        0,
                        32,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        160,
                        192,
                        224,
                        256,
                        320,
                        384,
                        0,
                    ],  # Layer 2
                    3: [
                        0,
                        32,
                        40,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        160,
                        192,
                        224,
                        256,
                        320,
                        0,
                    ],  # Layer 3
                },
                2: {  # MPEG 2 & 2.5
                    1: [
                        0,
                        32,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        144,
                        160,
                        176,
                        192,
                        224,
                        256,
                        0,
                    ],  # Layer 1
                    2: [
                        0,
                        8,
                        16,
                        24,
                        32,
                        40,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        144,
                        160,
                        0,
                    ],  # Layer 2
                    3: [
                        0,
                        8,
                        16,
                        24,
                        32,
                        40,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        144,
                        160,
                        0,
                    ],  # Layer 3
                },
            }

            # Sample rate table
            sample_rate_table = {
                1: [44100, 48000, 32000, 0],  # MPEG 1
                2: [22050, 24000, 16000, 0],  # MPEG 2
                2.5: [11025, 12000, 8000, 0],  # MPEG 2.5
            }

            # Get bitrate and sample rate from tables
            v_key = (
                1 if version == 1 else 2
            )  # Group MPEG 2 & 2.5 together for bitrate lookup
            bitrate = bitrate_table[v_key][layer][bitrate_index]
            sample_rate = sample_rate_table[version][sample_rate_index]

            if bitrate == 0 or sample_rate == 0:
                return None  # Invalid bitrate or sample rate

            # Check for VBR headers
            is_vbr = False
            total_frames = 0

            # Calculate offsets for Xing/VBRI headers
            xing_offset_from_frame = 36 if version == 1 else 21
            f.seek(offset + 4)  # Move past the frame header

            # Read enough data for possible VBR headers
            vbr_data = f.read(max(xing_offset_from_frame + 16, 36 + 16))

            # Check for Xing/Info header
            xing_pos = (
                xing_offset_from_frame - 4
            )  # Adjust for earlier read of frame header
            if len(vbr_data) > xing_pos + 4 and (
                vbr_data[xing_pos : xing_pos + 4] == b"Xing"
                or vbr_data[xing_pos : xing_pos + 4] == b"Info"
            ):
                # Check if frames field is present
                if len(vbr_data) > xing_pos + 8:
                    flags = (
                        (vbr_data[xing_pos + 4] << 24)
                        | (vbr_data[xing_pos + 5] << 16)
                        | (vbr_data[xing_pos + 6] << 8)
                        | vbr_data[xing_pos + 7]
                    )

                    if (flags & 0x1) and len(
                        vbr_data
                    ) > xing_pos + 12:  # Frames field present
                        total_frames = (
                            (vbr_data[xing_pos + 8] << 24)
                            | (vbr_data[xing_pos + 9] << 16)
                            | (vbr_data[xing_pos + 10] << 8)
                            | vbr_data[xing_pos + 11]
                        )
                        is_vbr = True

                        # Calculate duration based on frames and sample rate
                        samples_per_frame = 1152 if version == 1 else 576
                        duration_sec = total_frames * samples_per_frame / sample_rate
                        return str(int(duration_sec * 1000))

            # Check for VBRI header (less common)
            vbri_pos = 32  # VBRI is usually at fixed position from frame start
            if (
                len(vbr_data) > vbri_pos + 4
                and vbr_data[vbri_pos : vbri_pos + 4] == b"VBRI"
                and len(vbr_data) > vbri_pos + 18
            ):
                # Extract frames count
                total_frames = (
                    (vbr_data[vbri_pos + 14] << 24)
                    | (vbr_data[vbri_pos + 15] << 16)
                    | (vbr_data[vbri_pos + 16] << 8)
                    | vbr_data[vbri_pos + 17]
                )
                is_vbr = True

                # Calculate duration
                samples_per_frame = 1152 if version == 1 else 576
                duration_sec = total_frames * samples_per_frame / sample_rate
                return str(int(duration_sec * 1000))

            if not is_vbr:
                # For CBR, use file size method
                # Check for ID3v1 tag (128 bytes at the end)
                id3v1_size = 0
                f.seek(-128, 2)
                if f.read(3) == b"TAG":
                    id3v1_size = 128

                # Calculate audio size by removing tags
                audio_size = file_size - id3v2_size - id3v1_size

                # Calculate duration
                bitrate_bps = bitrate * 1000
                duration_sec = (audio_size * 8) / bitrate_bps
                return str(int(duration_sec * 1000))

    # OGG files
    elif file_ext == ".ogg":
        with open(file_path, "rb") as f:
            # Check for OggS signature
            header = f.read(4)
            if header != b"OggS":
                return None  # Not a valid OGG file

            # We need to find the last page's granule position and the sample rate
            # from an identification header
            sample_rate = 0
            granule_position = 0

            # Reset to beginning
            f.seek(0)

            # Read in chunks to find the sample rate and last granule position
            while True:
                # Read enough for Ogg page header
                page_header = f.read(27)
                if len(page_header) < 27:
                    break

                if page_header[0:4] != b"OggS":
                    # Try to resync
                    chunk = f.read(2048)
                    if not chunk:
                        break
                    sync_pos = chunk.find(b"OggS")
                    if sync_pos == -1:
                        continue
                    f.seek(-len(chunk) + sync_pos, 1)
                    continue

                # Extract granule position (64-bit)
                page_granule = int.from_bytes(page_header[6:14], byteorder="little")
                if page_granule > granule_position:
                    granule_position = page_granule

                # Get number of segments
                num_segments = page_header[26]

                # Read segment table
                segment_table = f.read(num_segments)
                if len(segment_table) < num_segments:
                    break

                # Calculate total size of all segments
                page_size = sum(segment_table)

                # If we haven't found sample rate and we're in the first 3 pages
                if sample_rate == 0 and f.tell() < 10000:
                    # Read this page's data to look for Vorbis header
                    page_data = f.read(min(page_size, 100))  # Only need beginning

                    # Look for Vorbis identification header pattern
                    vorbis_pos = page_data.find(b"\x01vorbis")
                    if vorbis_pos != -1 and vorbis_pos + 16 < len(page_data):
                        # Sample rate is at offset 12 from start of vorbis header
                        sr_pos = vorbis_pos + 12
                        if sr_pos + 4 <= len(page_data):
                            sample_rate = int.from_bytes(
                                page_data[sr_pos : sr_pos + 4], byteorder="little"
                            )
                    # Skip rest of page data if we read only part of it
                    if len(page_data) < page_size:
                        f.seek(page_size - len(page_data), 1)
                else:
                    # Skip page data
                    f.seek(page_size, 1)

            # If we found both granule position and sample rate, calculate duration
            if granule_position > 0 and sample_rate > 0:
                duration_sec = granule_position / sample_rate
                return str(int(duration_sec * 1000))

            return None

    # FLAC files
    elif file_ext == ".flac":
        with open(file_path, "rb") as f:
            # Check FLAC signature
            header = f.read(4)
            if header != b"fLaC":
                return None  # Not a FLAC file

            # Process metadata blocks
            is_last_block = False
            found_stream_info = False
            total_samples = 0
            sample_rate = 0

            while not is_last_block:
                # Read block header
                block_header = f.read(4)
                if len(block_header) < 4:
                    break

                is_last_block = (block_header[0] & 0x80) == 0x80
                block_type = block_header[0] & 0x7F
                block_length = (
                    (block_header[1] << 16) | (block_header[2] << 8) | block_header[3]
                )

                if block_type == 0:  # STREAMINFO block
                    if block_length >= 18:  # STREAMINFO is at least 18 bytes
                        stream_info = f.read(block_length)
                        if len(stream_info) >= 18:
                            # Extract sample rate (20 bits starting at byte 10)
                            sample_rate = (
                                (stream_info[10] << 12)
                                | (stream_info[11] << 4)
                                | ((stream_info[12] & 0xF0) >> 4)
                            )

                            # Extract total samples (36 bits starting at byte 13 bit 4)
                            total_samples = (
                                ((stream_info[13] & 0x0F) << 32)
                                | (stream_info[14] << 24)
                                | (stream_info[15] << 16)
                                | (stream_info[16] << 8)
                                | stream_info[17]
                            )
                            found_stream_info = True
                    else:
                        f.seek(block_length, 1)  # Skip this block
                else:
                    f.seek(block_length, 1)  # Skip this block

            if found_stream_info and sample_rate > 0:
                duration_sec = total_samples / sample_rate
                duration_ms = round(duration_sec * 1000)
                return str(duration_ms)

            return None

    # MP4/M4A files
    elif file_ext in [".mp4", ".m4a"]:
        with open(file_path, "rb") as f:
            # Find 'moov' atom by reading header chunks
            while True:
                atom_header = f.read(8)
                if not atom_header or len(atom_header) < 8:
                    break

                atom_size = int.from_bytes(atom_header[:4], byteorder="big")
                atom_type = atom_header[4:8]

                if atom_type == b"moov":
                    # Search for 'mvhd' atom inside 'moov'
                    moov_end = f.tell() + atom_size - 8
                    while f.tell() < moov_end:
                        sub_atom_header = f.read(8)
                        if not sub_atom_header or len(sub_atom_header) < 8:
                            break

                        sub_atom_size = int.from_bytes(
                            sub_atom_header[:4], byteorder="big"
                        )
                        sub_atom_type = sub_atom_header[4:8]

                        if sub_atom_type == b"mvhd":
                            # Skip version and flags
                            f.seek(4, 1)
                            # Skip creation time and modification time
                            f.seek(8, 1)
                            # Read time scale (frequency)
                            time_scale_data = f.read(4)
                            time_scale = int.from_bytes(
                                time_scale_data, byteorder="big"
                            )
                            # Read duration
                            duration_data = f.read(4)
                            duration_raw = int.from_bytes(
                                duration_data, byteorder="big"
                            )

                            if time_scale > 0:
                                duration = duration_raw / time_scale
                                return str(int(duration * 1000))
                            break

                        # Skip to the next sub-atom
                        if sub_atom_size > 8:
                            f.seek(sub_atom_size - 8, 1)
                    break

                # Skip to the next atom
                if atom_size > 8:
                    f.seek(atom_size - 8, 1)

    # If we can't determine the duration
    return None
