"    channel list: interior.Combined.R, interior.Combined.G, interior.Combined.B, interior.Combined.A, interior.Denoising Albedo Variance.R, interior.Denoising Albedo Variance.G, interior.Denoising Albedo Variance.B, interior.Denoising Albedo.R, interior.Denoising Albedo.G, interior.Denoising Albedo.B, interior.Denoising Depth Variance.Z, interior.Denoising Depth.Z, interior.Denoising Image Variance.R, interior.Denoising Image Variance.G, interior.Denoising Image Variance.B, interior.Denoising Normal Variance.Z, interior.Denoising Normal Variance.X, interior.Denoising Normal Variance.Y, interior.Denoising Normal.Z, interior.Denoising Normal.X, interior.Denoising Normal.Y, interior.Denoising Shadow A.V, interior.Denoising Shadow A.X, interior.Denoising Shadow A.Y, interior.Denoising Shadow B.V, interior.Denoising Shadow B.X, interior.Denoising Shadow B.Y, interior.Depth.Z, interior.Emit.R, interior.Emit.G, interior.Emit.B, interior.Noisy Image.R, interior.Noisy Image.G, interior.Noisy Image.B, interior.Noisy Image.A, interior.Vector.Z, interior.Vector.W, interior.Vector.X, interior.Vector.Y"

""" Explode multichannel exr into pfm files for use with intel denoiser """
""" Requires oiiotool and imagemagick on path """

import subprocess
import os
import argparse
import sys

# binary paths for subprocess
OIIOTOOL = ['oiiotool']
IMAGEMAGICK = ['convert'] if 'win' not in sys.platform else 'magick convert'

def main():
    def channel_array_to_oiiotool_string(channel_array):
        return str(channel_array).strip('[]').replace(', ',',')

    # parser = argparse.ArgumentParser()
    # parser.add_argument()

    # input_image = ''
    input_image = sys.argv[-1]
    input_image = os.path.abspath(input_image)
    dirname = os.path.dirname(input_image)
    print('reading: ', input_image)

    # Get channel names
    oiiotool_info = subprocess.check_output(['oiiotool', '-v', '--info', input_image]).decode('utf-8')
    channel_list = [s for s in oiiotool_info.split('\n') if 'channel list: ' in s][0]
    channel_list = channel_list.strip(' ')
    channel_list = channel_list.replace('channel list: ', '')
    channel_list = channel_list.split(', ')
    beauty_rgb = sorted([ch for ch in channel_list if '.Combined.' in ch and not ch.endswith('.A')], reverse=True)
    albedo_rgb = sorted([ch for ch in channel_list if '.Denoising Albedo.' in ch and not ch.endswith('.A')], reverse=True)
    normal_xyz = sorted([ch for ch in channel_list if '.Denoising Normal.' in ch])

    # Generate filenames
    basename = os.path.basename(input_image)
    filename = os.path.splitext(basename)[0]
    filepath = os.path.join(dirname, filename)

    oiiotool_conversions = {
            channel_array_to_oiiotool_string(beauty_rgb) : filepath + '_beauty.tif',
            channel_array_to_oiiotool_string(albedo_rgb) : filepath + '_albedo.tif',
            channel_array_to_oiiotool_string(normal_xyz) : filepath + '_normal.tif'
    }

    # Convert multichannel exr to single channel exrs
    for channel_string, intermediate_output in oiiotool_conversions.items():
        # Binary paths are lists to account for windows imagemagick needing two args [magick, convert]
        call_string = OIIOTOOL + [input_image, '-ch', channel_string.replace("'",''), '-o', intermediate_output]
        print('extracting channels: ', channel_string, ' to ', intermediate_output)
        
        # Convert single channel exrs to pfm files
        pfm_output = intermediate_output.replace('.tif', '.pfm')
        call_string = IMAGEMAGICK + [intermediate_output, '-endian', 'LSB', pfm_output]
        print('Converting ', intermediate_output, ' to ', pfm_output)
        subprocess.call(call_string)
        print('removing intermediate', intermediate_output)
        os.remove(intermediate_output)


if __name__ == '__main__':
    main()