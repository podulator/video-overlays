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

### The Script File - Required always
```javascript
{
    "_destination_movie": "%_FundraiserGuid_%", 
    "_output_path_prefix": "", 
    "_image_objects": [], 
    "_input_flags": "-strict -2", 
    "_output_encoders": [
		{
			"_extension": "mp4", 
			"_flags": "-profile:v main -level 3.1 -c:v libx264 -preset slow -crf 22 -threads 8"
		}, 
		{
			"_extension": "webm", 
			"_flags": "-c:v libvpx -quality good -cpu-used 5 -qmin 10 -qmax 42 -crf 18 -b:v 1M -c:a libvorbis -threads 8"
		}
    ],
    "_snapshot_name": "%_FundraiserGuid_%.png", 
    "_snapshot_timestamp": "00:00:03.123", 
    "_source_movie": "%_CWD_%/materials/JG 008 Animatic with TEXTLESS.mp4", 
    "_text_objects": [
        {
            "_alpha": 1.0, 
            "_border_colour": "black", 
            "_border_width": 0, 
            "_box": {
                "_border_width": 3, 
                "_colour": "0000AA99", 
                "_enabled": false, 
                "_opacity": 1.0
            }, 
            "_clean_content": true, 
            "_content": "Good luck %_FirstName_%", 
            "_fallback_content": "", 
            "_content_dirty": true, 
            "_content_max_length": 0, 
            "_drop_shadow": {
                "_colour": "black", 
                "_x": 0, 
                "_y": 0
            }, 
            "_fix_bounds": true, 
            "_font": {
                "_alpha": 1.0, 
                "_colour": "black", 
                "_family": null, 
                "_file": "%_CWD_%/materials/roboto_ttf/Roboto-Light.ttf", 
                "_size": 80
            }, 
            "_frame_from": 0, 
            "_frame_to": 97, 
            "_line_max_length": 50, 
            "_object_type": "drawtext", 
            "_x": "right-50", 
            "_y": 169.99
        }, 
        {
            "_alpha": 1.0, 
            "_border_colour": "silver", 
            "_border_width": 4, 
            "_box": {
                "_border_width": 3, 
                "_colour": "FF00AA00", 
                "_enabled": false, 
                "_opacity": 1.0
            }, 
            "_clean_content": true, 
            "_content": "%_CharityDisplayName_%", 
            "_fallback_content": "", 
            "_content_dirty": true, 
            "_content_max_length": 0, 
            "_drop_shadow": {
                "_colour": "black", 
                "_x": 0, 
                "_y": 0
            }, 
            "_fix_bounds": true, 
            "_font": {
                "_alpha": 1.0, 
                "_colour": "black", 
                "_family": null, 
                "_file": "%_CWD_%/materials/roboto_ttf/Roboto-Light.ttf", 
                "_size": 120
            }, 
            "_frame_from": 265, 
            "_frame_to": 348, 
            "_line_max_length": 30, 
            "_object_type": "drawtext", 
            "_x": "center", 
            "_y": "middle"
        }, 
        {
            "_alpha": 1.0, 
            "_border_colour": "black", 
            "_border_width": 0, 
            "_box": {
                "_border_width": 3, 
                "_colour": "FF00AA00", 
                "_enabled": false, 
                "_opacity": 1.0
            }, 
            "_clean_content": true, 
            "_content": "%_DonorMessage1_%", 
            "_fallback_content": "Fallback donation message #1", 
            "_content_dirty": true, 
            "_content_max_length": 0, 
            "_drop_shadow": {
                "_colour": "black", 
                "_x": 0, 
                "_y": 0
            }, 
            "_fix_bounds": true, 
            "_font": {
                "_alpha": 1.0, 
                "_colour": "black", 
                "_family": null, 
                "_file": "%_CWD_%/materials/roboto_ttf/Roboto-Light.ttf", 
                "_size": 80
            }, 
            "_frame_from": 453, 
            "_frame_to": 685, 
            "_line_max_length": 27, 
            "_object_type": "drawtext", 
            "_x": 0, 
            "_y": 0
        }
            "_alpha": 1.0, 
            "_border_colour": "black", 
            "_border_width": 0, 
            "_box": {
                "_border_width": 3, 
                "_colour": "FF00AA00", 
                "_enabled": false, 
                "_opacity": 1.0
            }, 
            "_clean_content": true, 
            "_content": "%_DonorMessage4_%", 
            "_fallback_content": "Fallback donation message #4", 
            "_content_dirty": true, 
            "_content_max_length": 0, 
            "_drop_shadow": {
                "_colour": "black", 
                "_x": 0, 
                "_y": 0
            }, 
            "_fix_bounds": true, 
            "_font": {
                "_alpha": 1.0, 
                "_colour": "black", 
                "_family": null, 
                "_file": "%_CWD_%/materials/roboto_ttf/Roboto-Light.ttf", 
                "_size": 80
            }, 
            "_frame_from": 819, 
            "_frame_to": 1052, 
            "_line_max_length": 27, 
            "_object_type": "drawtext", 
            "_x": 948, 
            "_y": 557
        }
    ]
}
```
* _destination_movie :: the name of the movie to render. No suffix as that is determined by each _output_encoders. Tokens are replaced.
* _output_path_prefix :: where to write the data to locally
* _input_flags :: any pre-processing flags, determined by the source movie
* _output_encoders :: a list of options setting the extension and flags to encode to
* _snapshot_name :: the name of the snapshot to create. Tokens are replaced.
* _snapshot_timestamp :: When in the movie to take the snapshot from
* _source_movie :: the source movie
* _text_objects :: a list of drawable objects
  * _alpha :: the text alpha value
  * _border_colour :: border colour if width set around the text
  * _border_width :: width of the border. 0 = no border
  * _box :: if we draw a box around the text, this defines it
  * _clean_content :: should we strip html tags etc
  * _content :: the content to render. Tokens are replaced
  * _fallback_content :: what to render if there is no _content
  * _content_max_length :: truncate to this length if we exceed. Zero means no truncate
  * _drop_shadow :: if we draw a drop shadow this defines it
  * _fix_bounds :: if true we try and force text to stay on the screen
  * _font :: this defines the font to use. _file tokens are replaced. ie. %_CWD_%/materials/path/to/font.ttf
  * _frame_from :: when does the text appear
  * _frame_to :: when does the text disappear
  * _line_length_max :: split to new line if we exceed this length. Don't split on zero
  * _x :: the x coord to draw from. origin (0, 0) is top left
    * magic values are left, center, right and can be combined with pixels. ie. right - 50
  * _y :: the y coord to draw from. origin (0, 0) is top left
    * magic values are top, middle, bottom and can be combined with pixels. ie. middle - 20
