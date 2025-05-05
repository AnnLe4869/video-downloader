from concurrent.futures import ThreadPoolExecutor
import subprocess
import fetching_m3u8

def download_m3u8(page_url: str, output_path: str):
    m3u8_files = fetching_m3u8.fetching_m3u8_requests(page_url)
    
    while len(m3u8_files) == 0:
        print("Retry getting " + page_url)
        m3u8_files = fetching_m3u8.fetching_m3u8_requests(page_url)
    
    ru_m3u8 = [f for f in m3u8_files if "miruro" not in f]
    
    for file in ru_m3u8:
        try:
            subprocess.run([
                "./yt-dlp.exe",
                file,
                "-o",
                output_path
            ], check=True)
            print(f"✅ Saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download {file}")
            print(e)
            
            
            
def main():
    # keep the ep number out
    base_url = "https://www.miruro.tv/watch?id=918&ep="
    base_output = "gintama-s01/gintama-"
    input_pairs = []
    # assuming episodes range from 1->n, just put n in there
    for i in range(200):
        input_pairs.append((
            base_url + str(i + 1),
            base_output + str(i + 1).zfill(2) + ".mp4"
        ))
        
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda pair: download_m3u8(*pair), input_pairs)
        
    # for i_pair in input_pairs:
    #     url, output = i_pair
    #     download_m3u8(url, output)
        
        
if __name__ == "__main__":
    main()