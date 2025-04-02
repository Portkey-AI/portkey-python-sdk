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
            buffer = f.read()

            # Skip ID3v2 tag if present
            offset = 0
            if buffer[0:3] == b"ID3":
                tag_size = (
                    ((buffer[6] & 0x7F) << 21)
                    | ((buffer[7] & 0x7F) << 14)
                    | ((buffer[8] & 0x7F) << 7)
                    | (buffer[9] & 0x7F)
                )
                offset = tag_size + 10

            # MPEG frame sync pattern: 11 bits set to 1 (0xFFE0)
            # Find first valid MPEG frame
            frame_header = None
            while offset < len(buffer) - 4:
                if buffer[offset] == 0xFF and (buffer[offset + 1] & 0xE0) == 0xE0:
                    frame_header = buffer[offset : offset + 4]
                    break
                offset += 1

            if not frame_header:
                return None  # No valid MPEG frame found

            # Extract version, layer, bitrate index, sample rate index, padding
            version_bits = (frame_header[1] & 0x18) >> 3
            layer_bits = (frame_header[1] & 0x06) >> 1
            frame_header[1] & 0x01
            bitrate_index = (frame_header[2] & 0xF0) >> 4
            sample_rate_index = (frame_header[2] & 0x0C) >> 2
            (frame_header[2] & 0x02) >> 1

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
            # Calculate CBR duration based on file size and bitrate
            # First, find file size excluding ID3 tags
            file_size = len(buffer)

            # Check for ID3v1 tag at the end (128 bytes)
            if file_size >= 128 and buffer[-128:-125] == b"TAG":
                file_size -= 128

            # Account for ID3v2 tag at the beginning
            if buffer[0:3] == b"ID3":
                tag_size = (
                    ((buffer[6] & 0x7F) << 21)
                    | ((buffer[7] & 0x7F) << 14)
                    | ((buffer[8] & 0x7F) << 7)
                    | (buffer[9] & 0x7F)
                )
                file_size -= tag_size + 10

            # For VBR files, try to find Xing or VBRI header
            is_vbr = False
            total_frames = 0

            # Check for Xing/Info header (common in VBR files)
            if version == 1:
                # MPEG 1: Xing header starts 36 bytes after the frame header
                xing_offset = offset + 4 + 32
            else:
                # MPEG 2/2.5: Xing header starts 21 bytes after the frame header
                xing_offset = offset + 4 + 17

            if xing_offset + 4 < len(buffer) and (
                buffer[xing_offset : xing_offset + 4] == b"Xing"
                or buffer[xing_offset : xing_offset + 4] == b"Info"
            ):
                # Check if frames field is present (bit 0 of flags)
                flags = (
                    (buffer[xing_offset + 4] << 24)
                    | (buffer[xing_offset + 5] << 16)
                    | (buffer[xing_offset + 6] << 8)
                    | buffer[xing_offset + 7]
                )

                if flags & 0x1:  # Frames field is present
                    total_frames = (
                        (buffer[xing_offset + 8] << 24)
                        | (buffer[xing_offset + 9] << 16)
                        | (buffer[xing_offset + 10] << 8)
                        | buffer[xing_offset + 11]
                    )
                    is_vbr = True

                    # Calculate duration based on frames and sample rate
                    if version == 1:
                        samples_per_frame = 1152  # MPEG 1 Layer 3
                    else:
                        samples_per_frame = 576  # MPEG 2/2.5 Layer 3

                    duration_sec = total_frames * samples_per_frame / sample_rate
                    return str(int(duration_sec * 1000))

            # VBRI header check (less common than Xing)
            vbri_offset = offset + 4 + 32  # VBRI is usually at a fixed position
            if (
                vbri_offset + 4 < len(buffer)
                and buffer[vbri_offset : vbri_offset + 4] == b"VBRI"
            ):
                # VBRI header has total frames at offset +14 (4 bytes)
                total_frames = (
                    (buffer[vbri_offset + 14] << 24)
                    | (buffer[vbri_offset + 15] << 16)
                    | (buffer[vbri_offset + 16] << 8)
                    | buffer[vbri_offset + 17]
                )
                is_vbr = True

                # Calculate duration based on frames and sample rate
                if version == 1:
                    samples_per_frame = 1152  # MPEG 1 Layer 3
                else:
                    samples_per_frame = 576  # MPEG 2/2.5 Layer 3

                duration_sec = total_frames * samples_per_frame / sample_rate
                return str(int(duration_sec * 1000))

            if not is_vbr:
                # Calculate bitrate in bits per second
                bitrate_bps = bitrate * 1000
                duration_sec = (file_size * 8) / bitrate_bps
                return str(int(duration_sec * 1000))

    # OGG files
    elif file_ext == ".ogg":
        with open(file_path, "rb") as f:
            buffer = f.read()

            # Check for OggS signature
            if not buffer.startswith(b"OggS"):
                return None  # Not a valid OGG file

            # First, look for the first Vorbis header packet
            # We need to find the identification header to get the sample rate
            sample_rate = 0
            granule_position = 0

            # Iterate through Ogg pages to find the last one and the sample rate
            offset = 0
            while offset < len(buffer) - 27:  # Minimum Ogg page header size is 27 bytes
                # Check for OggS capture pattern
                if buffer[offset : offset + 4] == b"OggS":
                    # Page header structure:
                    # 0-3: capture pattern "OggS"
                    # 4: stream structure version (0)
                    # 5: header type flag
                    # 6-13: granule position (64-bit)
                    # 14-17: stream serial number
                    # 18-21: page sequence number
                    # 22-25: CRC checksum
                    # 26: number of segments in the page

                    # Extract granule position (64-bit)
                    page_granule = (
                        (buffer[offset + 13] << 56)
                        | (buffer[offset + 12] << 48)
                        | (buffer[offset + 11] << 40)
                        | (buffer[offset + 10] << 32)
                        | (buffer[offset + 9] << 24)
                        | (buffer[offset + 8] << 16)
                        | (buffer[offset + 7] << 8)
                        | buffer[offset + 6]
                    )

                    if page_granule > granule_position:
                        granule_position = page_granule

                    # Get number of segments
                    num_segments = buffer[offset + 26]

                    segment_table_offset = offset + 27
                    segment_table_end = segment_table_offset + num_segments

                    if segment_table_end >= len(buffer):
                        break

                    # Calculate total size of all segments in this page
                    page_size = 27 + num_segments  # Header + segment table
                    for i in range(num_segments):
                        page_size += buffer[segment_table_offset + i]

                    # Check for Vorbis identification header in the first few pages
                    if sample_rate == 0 and offset < 10000:  # Only check the beginning
                        segment_data_offset = segment_table_end

                        # Look for Vorbis identification header pattern
                        for i in range(
                            segment_data_offset,
                            min(segment_data_offset + 40, len(buffer) - 7),
                        ):
                            if buffer[i] == 1 and buffer[i + 1 : i + 7] == b"vorbis":
                                if i + 16 < len(buffer):
                                    sample_rate = (
                                        (buffer[i + 15] << 24)
                                        | (buffer[i + 14] << 16)
                                        | (buffer[i + 13] << 8)
                                        | buffer[i + 12]
                                    )
                                    break

                    # Move to next page
                    offset += page_size
                else:
                    # If we lose sync, try to find the next "OggS" signature
                    start_idx = buffer.find(b"OggS", offset + 1)
                    if start_idx == -1:
                        break
                    offset = start_idx

            # If we found both the granule position and sample rate, calculate duration
            if granule_position > 0 and sample_rate > 0:
                duration_sec = granule_position / sample_rate
                return str(int(duration_sec * 1000))

            return None

    # FLAC files
    elif file_ext == ".flac":
        with open(file_path, "rb") as f:
            # Read the entire file into a buffer for easier manipulation
            buffer = f.read()

            # Check FLAC signature
            if buffer[0:4].decode("ascii", errors="ignore") != "fLaC":
                return None  # Not a FLAC file

            offset = 4
            is_last_block = False
            found_stream_info = False
            total_samples = 0
            sample_rate = 0

            while not is_last_block and offset < len(buffer):
                is_last_block = (buffer[offset] & 0x80) == 0x80
                block_type = buffer[offset] & 0x7F

                block_length = (
                    ((buffer[offset] & 0x7F) << 16)
                    | (buffer[offset + 1] << 8)
                    | buffer[offset + 2]
                )
                offset += 4

                if block_type == 0:  # STREAMINFO block
                    # Extract sample rate (20 bits)
                    sample_rate = (
                        (buffer[offset + 10] << 12)
                        | (buffer[offset + 11] << 4)
                        | ((buffer[offset + 12] & 0xF0) >> 4)
                    )

                    # Extract total samples (36 bits)
                    total_samples = (
                        ((buffer[offset + 13] & 0x0F) << 32)
                        | (buffer[offset + 14] << 24)
                        | (buffer[offset + 15] << 16)
                        | (buffer[offset + 16] << 8)
                        | buffer[offset + 17]
                    )

                    found_stream_info = True
                    break

                offset += block_length

            if not found_stream_info or sample_rate == 0:
                return None

            duration_sec = total_samples / sample_rate
            duration_ms = round(duration_sec * 1000)

            return str(duration_ms)

    # MP4/M4A files
    elif file_ext in [".mp4", ".m4a"]:
        with open(file_path, "rb") as f:
            # Find 'moov' atom
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
                            time_scale = int.from_bytes(f.read(4), byteorder="big")
                            # Read duration
                            duration_raw = int.from_bytes(f.read(4), byteorder="big")

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
