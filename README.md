# video-overlays
overlay images and text on a video from csv and ffmpeg script

## Running the transcoder
There are two ways to kick off the tool, 
1. from the cli
```bash
./video.py s3_bucket/path/to/config.json
./video.py -local
./video.py -help
```
* -local won't down or upload anything, so 
  * all supporting files are assumed ot be in place already, with a ./config.json file in place, and all materials under ./materials/
  * local files won't be deleted, they'll be left in ./outputs/
  * local logs won't be deleted

2. or falling back to user_data set at ec2 launch time which only supports the bucket config option, so your user data would look like :: s3_bucket/path/to/config.json

### The JSON Config File
```javascript
{
	"_create_html": true,
	"_create_movie": true, 
	"_create_snapshot": true, 
    "_data_file": "sample.csv", 
    "_data_definition_file": "data.definition", 
    "_data_has_headers": true, 
    "_data_seperator": "|", 
    "_html_output_file": "index.html", 
    "_html_template": "template.html", 
    "_max_rows": 10, 
    "_s3_destination": "video-transcodes-justgiving-com/my-story/%_PageShortName_%", 
    "_s3_materials": "video-transcodes-justgiving-com/config/materials", 
    "_script_file": "template.json", 
    "_terminate_on_completion": false
}
```
*   _create_html :: do we want an html file generated
*   _create_movie :: do we want a movie created
*   _create_snapshot :: do we want a snapshot created. Requires movie creation
*   _data_file :: the file in the materials folder to get our data from
*   _data_defintion_file :: the file in the materials folder that defines the tokens to swap for data for each row
*   _data_has_headers :: do we skip the first data row because it's got headers
*   _data_seperator :: sets if it's comma, tab or pipe seperated data
*   _html_output_file :: the name of the generated html file. Tokens are replaced
*   _html_template :: the name of the html template file. Tokens are replaced
*   _max_rows :: how much data to process, zero means all
*   _s3_destination :: where to upload all cretaed assets to. Tokens are replaced
*   _s3_materials :: where to get all the materials from. Downloaded to ./materials/
*   _script_file :: JSON file describing what to draw, when and where
*   _terminate_on_completion :: should the ec2 box suicide when done
### The Data File - Required always
This is a csv, seperated by
* comma
* tab
* pipe
It can have headers, skipable by setting _data_has_headers to true in the config file

### The Data Definition File - Required always
This is a csv file, comma seperated, containing the list of tokens in the same order as the data columns. The column count must match the _data_file column count. Tokens will be swapped for data for each row in the html template file, and in the script file for content and font file paths. There is a magic token appended to the end of this list, and every data row, %_CWD_%, which is the current directory, so paths can be fully qualified to the ./materials/ directory for fonts etc, as required by FFMPEG.

