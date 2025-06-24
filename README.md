Mô tả các Lab
==============================================

Hệ thống lab gồm 7 lab thực hiện các nhiệm vụ sau

* [steg_lsb73](https://github.com/mdt12345689/Custom_Lab/tree/main/steg_lsb73) Thực hiện giấu tin trên file audio với phương pháp 8 bit MSB và 3 bit LSB
* [lsb73_transfer_extract](https://github.com/mdt12345689/Custom_Lab/tree/main/lsb73_transfer_extract) Thực hiện tách tin trong file audio được giấu bằng phương pháp 8 bit MSB và 3 bit LSB
* [stego_audio_lsb84_embed](https://github.com/mdt12345689/Custom_Lab/tree/main/stego_audio_lsb84_embed) Thực hiện giấu tin trên file audio với phương pháp 8 bit MSB và 4 bit LSB
* [stego_audio_lsb84_extract](https://github.com/mdt12345689/Custom_Lab/tree/main/stego_audio_lsb84_extract) Thực hiện tách tin trong file audio được giấu bằng phương pháp 8 bit MSB và 4 bit LSB
* [compare_lsb](https://github.com/mdt12345689/Custom_Lab/tree/main/compare_lsb) So sánh 2 phương pháp trên với phương pháp giấu tin vào LSB đơn thuần
* [audio_stego_tool](https://github.com/mdt12345689/Custom_Lab/tree/main/audio_stego_tool) Thực hành cài đặt và sử dụng công cụ Audio Stego để giấu và tách tin vào audio


## Lý thuyết phương pháp và tham khảo
Please see the licensing and distribution information
in the [docs/license.md file](docs/license.md).

## Guide to directories

* scripts/labtainers-student -- the work directory for running and 
   testing student labs.  You must be in that directory to run 
   student labs.
   
* scripts/labtainers-instructor -- the work directory for 
   running and testing automated assessment and viewing student
   results.
  
* labs -- Files specific to each of the labs
   
* setup\_scripts -- scripts for installing Labtainers and Docker and updating Labtainers
   
* docs -- latex source for the labdesigner.pdf, and other documentation.

* UI -- Labtainers lab editor source code (Java).


January 24, 2018

-  Use of tabbed windows caused instructor side to fail, use of double quotes.
-  Ignore files in \_tar directories (other than .tar) when determining build
   dependencies.

