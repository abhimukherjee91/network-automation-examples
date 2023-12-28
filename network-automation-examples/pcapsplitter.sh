#!/bin/sh
## Auther: Abhi Mukherjee
##This shell script splits large size pcap/pcapng files into smaller pieces in-order for them to download easily. You will need to provide the original file name along with file-size (in Mb) of the indiviual chunks. ex: ./pcapsplitter.sh example.pcap 1024. This spitls example.pcap into multiple pcap files each having 1024 Mb size.

while getopts ":h" option; do
   case $option in
      h) # display Help
         echo "Usage: ./pcapsplitter.sh <original-PCAP-filename> <Size-of-individual-chunk-in-Mb>"
         exit;;
   esac
done
if [ -z "$1" ]
then
        echo "Source capture file name not provided"
        exit 1;
fi
if [ -z "$2" ]
then
        echo "Individual capture file-size not provided"
        exit 1;
fi
split_ext=$(echo "$1" | cut -d "." -f 2)
if [[ $split_ext != pcap* ]]
then
    echo "Not a valid extention. Only "pcap" and "pcapng" are supported"
    exit 1
fi
split_filename=$(echo "$1" | cut -d "." -f 1)
split_filename="${split_filename}-split"
tcpdump -r "$1" -w "$split_filename" -C "$2"
files=$(ls -ltr | grep "$split_filename" | awk '{print $9}')
for file in $files
do
final_filename="$file"."$split_ext"
mv "$file" "$final_filename"
echo $final_filename
done
