#!/bin/bash

# Rename the file back to its original name
mv "C:\Users\JGI\Downloads\Form_3018_Rockwell_2025-01-31.xlsm" "C:\Users\JGI\Downloads\Form_3018_Rockwell.xlsm"

# Run the validate_upload.sh script
bash "C:\Users\JGI\Desktop\ci-scripts\validate_upload.sh"
