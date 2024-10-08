import os
import json
import time
import requests
import argparse

# STATIC
##########################################################
morph_file_std = "https://neuromorpho.org/dableFiles/{}/CNG%20version/{}.CNG.swc"
morph_file_og = "https://neuromorpho.org/dableFiles/{}/Source-Version/{}.txt"
log_file_std = "https://neuromorpho.org/dableFiles/{}/Remaining issues/{}.CNG.swc.std"
log_file_og = "https://neuromorpho.org/dableFiles/{}/Standardization log/{}.std"
##########################################################




# Function to fetch a single page of results
def fetch_page(archive, species, page):
    if archive is not None: 
        url = f"http://cng.gmu.edu:8080/api/neuron/select?q=archive:{archive}&fq=species:{species}&page={page}"
    else:
        url = f"http://cng.gmu.edu:8080/api/neuron/select?q=species:{species}&page={page}"
    response = requests.get(url)
    
    # Check if the request is successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching page {page}: {response.status_code}")
        return None

# Function to iterate through pages and download all data
def fetch_all_data(archive, species):
    all_neurons = []
    page = 0
    while True:
        print(f"Fetching page {page}...")
        data = fetch_page(archive, species, page)
        
        if not data:
            break  # Stop if the response is invalid
        
        # Check if there are neurons in the current page
        if '_embedded' in data and 'neuronResources' in data['_embedded']:
            neurons = data['_embedded']['neuronResources']
            all_neurons.extend(neurons)  # Add neurons to the full list
            
            # If the number of neurons is less than 50, it means there are no more pages
            if len(neurons) < 50:
                break
        else:
            break  # Stop if no neurons are found
        
        page += 1  # Increment to the next page
        time.sleep(4)  # Pause to avoid overloading the server

    return all_neurons

# Function to download an SWC file for a given neuron
def download_swc_file(neuron, output_folder, file_type='std'):
    neuron_name = neuron['neuron_name']
    archive_name = neuron['archive']

    # Choose the URL based on file type (standardized or original)
    if file_type == 'std':
        swc_url = morph_file_std.format(archive_name.lower(), neuron_name)
        file_extension = '.CNG.swc'
    else:
        swc_url = morph_file_og.format(archive_name.lower(), neuron_name)
        file_extension = '.txt'

    # Define the path where the SWC file will be saved
    output_path = os.path.join(output_folder, f"{neuron_name}{file_extension}")

    try:
        # Download the SWC file
        print(f"Downloading {neuron_name}...")
        response = requests.get(swc_url)

        # Check if the download was successful
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {output_path}")
        else:
            print(f"Failed to download {neuron_name}. Status code: {response.status_code}")
        #os.system(f"wget {swc_url} -P {output_folder}")

    except Exception as e:
        print(f"Error downloading {neuron_name}: {e}")

# Function to iterate through the neurons and download SWC files
def download_all_swc_files(metadata_filename, output_folder, file_type='std'):
    # Load the neuron metadata from the previously saved JSON file
    with open(os.path.join(output_folder, metadata_filename), 'r') as f:
        neuron_metadata = json.load(f)

    # Iterate through each neuron and download its SWC file
    for neuron in neuron_metadata:
        download_swc_file(neuron, output_folder, file_type=file_type)
        time.sleep(5)  # Small delay to avoid overwhelming the server







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root", type=str, default=None, help="Specify data download directory. (Default set to current directory)")
    parser.add_argument("--species", type=str, default="zebrafish", help="Enter species to download. See neuromorpho.org for more details. Default is zebrafish.")
    parser.add_argument("--archive", type=str, default=None, help="Specify archive name. Default is None. Do not specify if you want the full records.")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()

    root = args.data_root
    species = args.species
    archive = args.archive

    if args.data_root == None: root = "." #os.getcwd()
    save = True
    fetch = args.fetch
    download = args.download
    filename = f"{species}_{archive}.json" if archive is not None else f"{species}_full.json"
    output_folder = f"{root}/{species}_{archive}" if archive is not None else f".{root}/{species}_full"
    os.makedirs(output_folder, exist_ok=True)

    if fetch:
        print('Fetching Metadata')
        # Fetch all neurons and save them
        all_neurons = fetch_all_data(archive, species)

        # Save to a JSON file
        if save:
            with open(os.path.join(output_folder, filename), 'w') as f:
                json.dump(all_neurons, f, indent=4)

        print(f"Total neurons fetched: {len(all_neurons)}")
        print(f"Data saved to {filename}")

    if download:
        #Load json
        with open(os.path.join(output_folder, filename), 'rb') as f:
            data = json.load(f)
        time.sleep(2)

        print(f"Found {len(data)} neurons in total!")
        print("Commencing download:")
        download_all_swc_files(filename, output_folder, file_type='std')