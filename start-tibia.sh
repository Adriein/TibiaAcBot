#!/bin/bash

# Open the first terminal tab, navigate to directory and run command
gnome-terminal --tab --working-directory="/home/aclaret/Programs/Tibia" --command="bash -c './start-tibia-launcher.sh ; exec bash'"

# Open the second terminal tab, navigate to another directory and run command
gnome-terminal --tab --working-directory="/home/aclaret/CLARET-DEV/TibiaAcBot"

# Open OBS
obs