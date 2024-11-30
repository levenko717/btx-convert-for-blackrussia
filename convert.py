import os
import sys
import PVRTexLibPy as pvrpy

def convert_png_to_btx(png_path):
    if not os.path.isfile(png_path):
        print(f"Файл не найден: {png_path}")
        return
    
    texture = pvrpy.PVRTexture(png_path)

    # Преобразование к текстуре
    if not texture.PreMultiplyAlpha():
        print('Ошибка при конвертации файла 1')
        os.remove(png_path)
        return

    if not texture.Bleed():
        print('Ошибка при конвертации файла 2')
        os.remove(png_path)
        return

    if not texture.Transcode(pvrpy.PixelFormat.ASTC_4x4, pvrpy.VariableType.UnsignedByteNorm, pvrpy.ColourSpace.sRGB,
                             pvrpy.CompressorQuality.ASTCExhaustive):
        print('Ошибка при конвертации файла 3')
        os.remove(png_path)
        return

    if texture.SetTextureColourSpace(pvrpy.ColourSpace.Linear) == False:
        print('Ошибка при конвертации файла 4')
        os.remove(png_path)
        return

    ktx_path = os.path.splitext(png_path)[0] + ".ktx"
    if not texture.SaveToFile(ktx_path):
        print('Ошибка при конвертации файла 5')
        os.remove(png_path)
        return

    with open(ktx_path, 'r+b') as ktx_file:
        original_bytes = ktx_file.read()
        ktx_file.seek(0)
        ktx_file.write(b'\x02\x00\x00\x00')
        ktx_file.write(original_bytes)

    os.rename(ktx_path, os.path.splitext(ktx_path)[0] + '.btx')
    print(f"Конвертация завершена, файл сохранен как: {ktx_path.replace('.ktx', '.btx')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python <путь_к_скрипту> <путь_к_png>")
    else:
        convert_png_to_btx(sys.argv[1])
