# PixelLinerTranslate
## Install translated version
Currently, Chinese version of PixelLiner 0.97.15 is provided. Although the translated version looks good to me, since I do not have much translation experience, there might be flaws in translation results. I encourage creating your own translation version with tool provided. 
### Install translated release
Download releases at here:
| Version | Link |
| --- | --- |
| Chinese | [Release Link](https://github.com/DreamRuthenium/PixelLinerTranslate/releases/download/CH/PixelLiner_CH_1.0.0.zip) |

Inside each pack, there's a .swf file and a .air file. You chan chose one method to install. Both method requires installing Adobe Air before. You can download it from [here](https://airsdk.harman.com/runtime).

#### Method 1(When you have PixelLiner already installed)
Replace pxl.swf in installation path.

#### Method 2(When you do not have PixelLiner installed): 
Simply click the .air file and install it. 

Notice: Since I don't have the original certificate, replace versions that have been installed from official website would throw a "Certificate don't match" error. In that case, you need to uninstall original version, then try installation again.


## Make my own translation
### Setup
#### Crack tool setup
Download *release version* of [RABCDAsm](https://github.com/CyberShadow/RABCDAsm) and unzip it into `./RABCDAsm` (The executable file should be directly accessible in `./RABCDAsm`, please avoid structures like `./RABCDAsm/RABCDAsm`).

```
curl.exe -L "https://github.com/CyberShadow/RABCDAsm/releases/download/1.18/RABCDAsm_v1.18.7z" -o "RABCDAsm.7z"
```
```
tar -xf "RABCDAsm.7z" -C "./RABCDAsm"
```

#### Python setup
Python version: 3.14.0. There's no special packages that requires to be installed.

#### Apache Ant setup(optional)
Apache Ant allows you to repackage translated .swf files into air installation package. However, simply replace .swf file in installation path is also a feasible approach.

Firstly, you need an JDK with version higher than JDK8(17 is recommended) installed. Then, you should add java home into path, so it can be found by Apache Ant.

Secondly, download AIR SDK from [here](https://airsdk.harman.com/download), and install it.

Simple check if ant works:
```
ant -version
```

You should get message like:
```
Apache Ant(TM) version 1.10.1 compiled on February 2 2017
```

#### PixelLiner Download
Download the version of PixelLiner that you want to translate from [here](https://pixelliner.sakura.ne.jp/wiki/index.php?Download). Then, move the .air file into `./air` folder.

Good! you are ready to go!

