import os
import zstandard as zstd

def pmtok_compress(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.bfres'):
                bfres_file_path = os.path.join(root, file)
                output_file = f"{bfres_file_path}.zst"
                cctx = zstd.ZstdCompressor()
                with open(bfres_file_path, 'rb') as f_in, open(output_file, 'wb') as f_out:
                    compressed_data = cctx.compress(f_in.read())
                    f_out.write(compressed_data)
                zst_filename = os.path.basename(output_file)
                # bfres_filename = os.path.basename(bfres_file_path)
                print(f"Compressed {zst_filename}")
                os.remove(bfres_file_path)
                # print(f"Deleted {bfres_filename}")
