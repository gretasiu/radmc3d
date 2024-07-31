#!/bin/bash

# # Set up environment for graphical applications
# export DISPLAY=:1

# Function to handle cleanup and exit
cleanup() {
    echo "Script interrupted. Exiting..."
    exit 1
}
# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT

template_dir="/home/gsiu/parameter_search/template_v4_toroidal_auto"

# Define the step to run
#step_to_run="inp,radimage,radvis,synobs,tclean,visan"  # Change this variable to the desired step
step_to_run="inp,radimage,radvis"

# Define parameters with their respective values
declare -A parameters
parameters=(
    ["scaling"]=40
    ["pitchness"]=1000
    ["rotation_per"]=1
    ["rotation_power"]=2
    ["npix"]=1000
    ["incl"]="25 45 60 90 "
    ["phi"]=0
    ["posang"]=0
    ["sizeau1300"]=40000
    ["sizeau7000"]=40000
)

#"25 45 90"
#"0 45 90 135 180 225 270 315" 

copy_fig(){
    local new_dir="$1"
    local fig_dir="$2"

    # Extract parameter combination from the new directory name
    local param_combination=$(basename "$new_dir" | sed 's/trial_//')

    # Rename the fig directory and copy to centralized directory
    local new_fig_dir="${fig_dir}/fig_${param_combination}"
   
    # Remove the existing directory if it exists
    if [ -d "$new_fig_dir" ]; then
        rm -rf "$new_fig_dir"
    fi
   
    cp -r "${new_dir}/fig" "$new_fig_dir"
}

check_dir_exsistence(){
    # Check if the directory already exists
    if [ -d "$new_dir" ]; then
        echo "Error: Directory '$new_dir' already exists. Exiting."
        exit 1
    fi
}

# Function to replace placeholders in files
replace_placeholders() {
    local file_path="$1"

    for placeholder in "${!parameters[@]}"; do
        local replacement="${parameters[$placeholder]}"
        # Ensure the replacement is properly formatted without quotes
        if [[ "$replacement" =~ ^[0-9]+$ || "$replacement" =~ ^[0-9]*\.[0-9]+$ ]]; then
            # Replace placeholders wrapped in single quotes
            sed -i "s/'${placeholder}_PLACEHOLDER'/${replacement}/g" "$file_path"
        else
            # Replace placeholders not wrapped in quotes
            sed -i "s/${placeholder}_PLACEHOLDER/${replacement}/g" "$file_path"
        fi
    done
}

# Function to create README.md file
create_readme() {
    local directory="$1"

    local readme_path="$directory/README.md"
    {
        echo "# Parameter Details"
        echo ""
        echo "Parameters used for this directory:"
        for key in "${!parameters[@]}"; do
            echo "- $key: ${parameters[$key]}"
        done
    } > "$readme_path"
}

# Function to generate all combinations of parameters
generate_combinations() {
    local keys=()
    local values=()

    for key in "${!parameters[@]}"; do
        if [[ ! "${parameters[$key]}" =~ ^[0-9]+$ && ! "${parameters[$key]}" =~ ^[0-9]*\.[0-9]+$ ]]; then
            keys+=("$key")
            values+=("${parameters[$key]}")
        fi
    done

    local combinations=()
    combinations+=("")

    for i in "${!keys[@]}"; do
        local key="${keys[$i]}"
        IFS=' ' read -r -a value_list <<< "${values[$i]}"
        local new_combinations=()

        for combo in "${combinations[@]}"; do
            for value in "${value_list[@]}"; do
                new_combinations+=("${combo}${key}=${value} ")
            done
        done
        combinations=("${new_combinations[@]}")
    done

    # Join combinations with commas
    local combined_combinations=$(IFS=','; echo "${combinations[*]}")

    # # Debug print to verify combinations
    # for combo in "${combinations[@]}"; do
    #     echo "$combo"
    # done

    # Debug print to verify combinations
    # echo "Generated combinations:"
    echo "$combined_combinations"
}

perform_search() {
    local combined_string="$1"
    IFS=',' read -r -a combinations <<< "$combined_string"

    for combination in "${combinations[@]}"; do
        # Remove leading/trailing whitespace
        combination=$(echo "$combination" | xargs)
        
        # Check if combination is not empty
        if [ -z "$combination" ]; then
            continue
        fi

        local param_combination=""
        local replacements=""

        # Create sanitized directory name
        local new_dir="trial_$(echo "$combination" | tr ' ' '_' | sed 's/[= ]/_/g')"
        
        check_dir_exsistence
        
        mkdir -p "$new_dir"  # Create directory if it does not exist
        echo "Creating directory: $new_dir"  # Debug print
        cp -r "$template_dir"/* "$new_dir"

        # Update parameters in new directory
        # Use a temporary array to capture the updated parameters
        declare -A temp_parameters

        #echo "Original parameters: ${!parameters[@]}=${parameters[@]}"  # Debug print for original parameters

        # Split the combination into key-value pairs by whitespace
        IFS=' ' read -r -a pairs <<< "$combination"
        for pair in "${pairs[@]}"; do
            # Split each pair by '=' to get key and value
            IFS='=' read -r key value <<< "$pair"
            
            # Remove leading/trailing '=' from key and value
            key=$(echo "$key" | sed 's/^[=]*//; s/[=]*$//')
            value=$(echo "$value" | sed 's/^[=]*//; s/[=]*$//')

            # Store the key-value pair in the temporary array
            temp_parameters[$key]=$value
        done

        # Apply the temporary parameters to the global parameters
        for key in "${!temp_parameters[@]}"; do
            parameters[$key]=${temp_parameters[$key]}
        done

        # # Debug print to show updated parameters
        # echo "Updated parameters for combination '${combination}':"
        # for key in "${!parameters[@]}"; do
        #     echo "$key=${parameters[$key]}"
        # done

        replace_placeholders "$new_dir/setup.py"
        replace_placeholders "$new_dir/plotimage.py"

        chmod +x "$new_dir/exe.sh"
        (cd "$new_dir" && ./exe.sh "$step_to_run")

        # Copy figs to centralized directory with appropriate renaming
        copy_fig "$new_dir" "$fig_dir"

        create_readme "$new_dir"

        echo "Search for parameter combination '${combination}' completed."
    done
}

# Determine the type of parameters
list_params=()
non_list_params=()

for key in "${!parameters[@]}"; do
    if [[ "${parameters[$key]}" =~ ^[0-9]+$ || "${parameters[$key]}" =~ ^[0-9]*\.[0-9]+$ ]]; then
        non_list_params+=("$key")
    else
        list_params+=("$key")
    fi
done

if [ ${#list_params[@]} -eq 0 ]; then
    # Scenario 1: All parameters are single values
    timestamp=$(date +%Y%m%d_%H%M%S)
    new_dir="trial_default_${timestamp}"

    check_dir_exsistence

    echo "Creating directory ${new_dir}"    
    mkdir -p "$new_dir"
    cp -r "$template_dir"/* "$new_dir"

    replace_placeholders "$new_dir/setup.py"
    replace_placeholders "$new_dir/plotimage.py"

    chmod +x "$new_dir/exe.sh"
    (cd "$new_dir" && ./exe.sh "$step_to_run")

    create_readme "$new_dir"

    echo "One-off parameter setup completed."

elif [ ${#list_params[@]} -eq 1 ]; then
    # Scenario 2: Only one parameter is a list
    list_param="${list_params[0]}"
    values=(${parameters[$list_param]})

    # Create a centralized directory for figures
    timestamp=$(date +%Y%m%d_%H%M%S)
    fig_dir="fig_${timestamp}"
    mkdir -p "$fig_dir"
    create_readme "$fig_dir"

    for value in "${values[@]}"; do
        new_dir="trial_${list_param}_$value"

        check_dir_exsistence

        echo "Creating directory ${new_dir}"
        mkdir -p "$new_dir"

        cp -r "$template_dir"/* "$new_dir"

        # Set the list parameter value
        parameters[$list_param]=$value

        replace_placeholders "$new_dir/setup.py"
        replace_placeholders "$new_dir/plotimage.py"

        chmod +x "$new_dir/exe.sh"
        (cd "$new_dir" && ./exe.sh "$step_to_run")

        # Copy figs to centralized directory with appropriate renaming
        copy_fig "$new_dir" "$fig_dir"
        
        create_readme "$new_dir"

        echo "Search for parameter ${list_param}=${value} completed."
    done

else
    # Scenario 3: More than one parameter is a list

    # Create a centralized directory for figures
    timestamp=$(date +%Y%m%d_%H%M%S)
    fig_dir="fig_${timestamp}"
    mkdir -p "$fig_dir"
    create_readme "$fig_dir"

    combinations=$(generate_combinations)
    
    echo "Generated combinations:"
    echo "$combinations"

    perform_search "$combinations"
fi
