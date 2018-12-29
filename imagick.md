# Imagick

## Magic Number
768

```
./coders/gif.c:1562:  global_colormap=(unsigned char *) AcquireQuantumMemory(768UL,
./coders/gif.c:1564:  colormap=(unsigned char *) AcquireQuantumMemory(768UL,sizeof(*colormap));

  for (i=0; i < 768; i++)
    colormap[i]=(unsigned char) 0;
```

## 坑
setFormat / setImageFormat

## GMagick

### Installation

#### issue 1
```
Uncaught GmagickException: No decode delegate for this image format (/home/work/Projects/BotGames/CaiShangBiao/resources/background.png)

checking for PNG support ...
checking png.h usability... no
checking png.h presence... no
checking for png.h... no
checking for gs color+alpha device... pngalpha
PNG               --with-png=yes          	no

./configure CFLAGS="-I/home/work/.jumbo/include -g -Og" CXXFLAGS="-g -Og" --prefix=/usr/local --with-x=no --enable-shared | fgrep -i --color png -C3
```

#### issue2
```
      "error_info": {
        "error_type": 3503,
        "error_msg": "Request Time Out"
      }
```

./configure CFLAGS="-g -Og -I/home/work/.jumbo/include/libpng16" LDFLAGS="-L/home/work/.jumbo/lib" LIBS="-lpng16" PKG_CONFIG=$(which pkg-config) --prefix=/usr/local --with-x=no --enable-shared

```
./configure CFLAGS="-g -Og " CXXFLAGS="-g -Og" --prefix=/usr/local --with-x=no --enable-shared

./configure CFLAGS="-g -Og" CXXFLAGS="-g -Og" PKG_CONFIG=$(which pkg-config) --prefix=/usr/local --with-x=no --enable-shared

$ gm version
```

```
GraphicsMagick is configured as follows. Please verify that this
configuration matches your expectations.

Host system type : x86_64-pc-linux-gnu
Build system type : x86_64-pc-linux-gnu

Option            Configure option      	Configured value
-----------------------------------------------------------------
Shared libraries  --enable-shared=yes		yes
Static libraries  --enable-static=yes		yes
GNU ld            --with-gnu-ld=yes    		yes
Quantum depth     --with-quantum-depth=8	8
Modules           --with-modules=no  		no

Delegate Configuration:
BZLIB             --with-bzlib=yes         	yes
DPS               --with-dps=yes          	no
FlashPIX          --with-fpx=no          	no
FreeType 2.0      --with-ttf=yes          	no (failed tests)
Ghostscript       None                  	gs (7.07)
Ghostscript fonts --with-gs-font-dir=default	/usr/share/fonts/default/Type1/
JBIG              --with-jbig=yes        	no
JPEG v1           --with-jpeg=yes        	no
JPEG-2000         --with-jp2=yes          	no
LCMS v2           --with-lcms2=yes        	no
LZMA              --with-lzma=yes        	yes
Magick++          --with-magick-plus-plus=yes	yes
PERL              --with-perl=no        	no
PNG               --with-png=yes          	no
TIFF              --with-tiff=yes        	no
TRIO              --with-trio=yes        	no
WEBP              --with-webp=yes        	no
Windows fonts     --with-windows-font-dir=	none
WMF               --with-wmf=yes          	no
X11               --with-x=no              	no
XML               --with-xml=yes          	yes
ZLIB              --with-zlib=yes        	yes

X11 Configuration:

  Not using X11.

Options used to compile and link:
  CC       = gcc -std=gnu99
  CFLAGS   = -fopenmp -g -Og -Wall -pthread
  CPPFLAGS = -I/home/work/.jumbo/include/freetype2 -I/home/work/.jumbo/include/libxml2
  CXX      = g++
  CXXFLAGS = -g -Og -pthread
  DEFS     = -DHAVE_CONFIG_H
  LDFLAGS  = -L/home/work/.jumbo/lib
  LIBS     = -llzma -lbz2 -lxml2 -lz -lm -lpthread
```

```
==============================================================================
ImageMagick is configured as follows. Please verify that this configuration
matches your expectations.

  Host system type: x86_64-pc-linux-gnu
  Build system type: x86_64-pc-linux-gnu

                 Option                        Value
  ------------------------------------------------------------------------------
  Shared libraries  --enable-shared=yes		yes
  Static libraries  --enable-static=yes		yes
  Build utilities   --with-utilities=yes        yes
  Module support    --with-modules=no		no
  GNU ld            --with-gnu-ld=yes		yes
  Quantum depth     --with-quantum-depth=16	16
  High Dynamic Range Imagery
                    --enable-hdri=yes		yes

  Install documentation:			yes

  Delegate Library Configuration:
  BZLIB             --with-bzlib=yes		yes
  Autotrace         --with-autotrace=no		no
  DJVU              --with-djvu=yes		no
  DPS               --with-dps=yes		no
  FFTW              --with-fftw=yes		no
  FLIF              --with-flif=yes		no
  FlashPIX          --with-fpx=yes		no
  FontConfig        --with-fontconfig=yes	no
  FreeType          --with-freetype=yes		yes
  Ghostscript lib   --with-gslib=no		no
  Graphviz          --with-gvc=yes		no
  HEIC              --with-heic=yes             no
  JBIG              --with-jbig=yes		no
  JPEG v1           --with-jpeg=yes		no
  LCMS              --with-lcms=yes		no
  LQR               --with-lqr=yes		no
  LTDL              --with-ltdl=yes		no
  LZMA              --with-lzma=yes		yes
  Magick++          --with-magick-plus-plus=yes	yes
  OpenEXR           --with-openexr=yes		no
  OpenJP2           --with-openjp2=yes		no
  PANGO             --with-pango=yes		no
  PERL              --with-perl=no		no
  PNG               --with-png=yes		yes
  RAQM              --with-raqm=yes		no
  RAW               --with-raw=yes 	   	no
  RSVG              --with-rsvg=no		no
  TIFF              --with-tiff=yes		no
  WEBP              --with-webp=yes		no
  WMF               --with-wmf=yes		no
  X11               --with-x=no			no
  XML               --with-xml=yes		yes
  ZLIB              --with-zlib=yes		yes
  ZSTD              --with-zstd=yes		no

  Delegate Program Configuration:
  GhostPCL          None				pcl6 (unknown)
  GhostXPS          None				gxps (unknown)
  Ghostscript       None				gs (7.07)

  Font Configuration:
  Apple fonts       --with-apple-font-dir=default
  Dejavu fonts      --with-dejavu-font-dir=default	none
  Ghostscript fonts --with-gs-font-dir=default	/usr/share/fonts/default/Type1/
  URW-base35 fonts  --with-urw-base35-font-dir=default  none
  Windows fonts     --with-windows-font-dir=default	none

  X11 Configuration:
        X_CFLAGS        =
        X_PRE_LIBS      =
        X_LIBS          =
        X_EXTRA_LIBS    =

  Options used to compile and link:
    PREFIX          = /usr/local
    EXEC-PREFIX     = /usr/local
    VERSION         = 7.0.8
    CC              = gcc -std=gnu99 -std=gnu99
    CFLAGS          = -I/home/work/.jumbo/include/libxml2  -I/home/work/.jumbo/include/libpng16  -I/home/work/.jumbo/include  -I/home/work/.jumbo/include/freetype2 -I/home/work/.jumbo/include -I/home/work/.jumbo/include/libpng16  -I/home/work/.jumbo/include   -fopenmp -g -Og  -Wall -mtune=core-avx2 -fexceptions -pthread -DMAGICKCORE_HDRI_ENABLE=1 -DMAGICKCORE_QUANTUM_DEPTH=16
    CPPFLAGS        =   -DMAGICKCORE_HDRI_ENABLE=1 -DMAGICKCORE_QUANTUM_DEPTH=16
    PCFLAGS         =
    DEFS            = -DHAVE_CONFIG_H
    LDFLAGS         =
    LIBS            =     -L/home/work/.jumbo/lib -lfreetype      -L/home/work/.jumbo/lib -lpng16                 -L/home/work/.jumbo/lib -llzma  -lbz2      -L/home/work/.jumbo/lib -lxml2   -L/home/work/.jumbo/lib -lz      -lm
    CXX             = g++
    CXXFLAGS        = -g -Og -pthread
    FEATURES        = DPC HDRI Cipher OpenMP
    DELEGATES       = bzlib mpeg freetype lzma png ps xml zlib
==============================================================================
```

```php
#0  WriteGIFImage (image_info=0x142e020, image=0x13c5610, exception=0x138ffc0) at coders/gif.c:1508
#1  0x00007ffff171ed00 in WriteImage (image_info=image_info@entry=0x142ad30, image=image@entry=0x13c5610, exception=exception@entry=0x138ffc0) at MagickCore/constitute.c:1161
#2  0x00007ffff171f25e in WriteImages (image_info=image_info@entry=0x1413a30, images=<optimized out>, images@entry=0x13c5610, filename=filename@entry=0x13c5a08 "",
    exception=exception@entry=0x138ffc0) at MagickCore/constitute.c:1378
#3  0x00007ffff16f077a in ImagesToBlob (image_info=0x13a0000, images=0x13c5610, length=length@entry=0x7fffffffafd0, exception=exception@entry=0x138ffc0) at MagickCore/blob.c:2433
#4  0x00007ffff1cf8aff in MagickGetImagesBlob (wand=0x1399a20, length=0x7fffffffafd0) at MagickWand/magick-image.c:3941
#5  0x00007ffff1fcca41 in zim_imagick_getimagesblob (execute_data=0x7ffff58142f0, return_value=0x7ffff58142e0) at /home/work/Downloads/imagick-3.4.3/imagick_class.c:8376
```

```
    1673        for (i=0; i < (ssize_t) image->colors; i++)
    1674        {
    1675          *q++=ScaleQuantumToChar(ClampToQuantum(image->colormap[i].red));
    1676          *q++=ScaleQuantumToChar(ClampToQuantum(image->colormap[i].green));
    1677          *q++=ScaleQuantumToChar(ClampToQuantum(image->colormap[i].blue));
    1678        }
    1679        for ( ; i < (ssize_t) (one << bits_per_pixel); i++)
    1680        {
    1681          *q++=(unsigned char) 0x0;
    1682          *q++=(unsigned char) 0x0;
    1683          *q++=(unsigned char) 0x0;
    1684        }
```

