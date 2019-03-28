import scrape_data as scrape
import clean_data as clean
import push_data as push

def run_pipeline():
    # Get guitar brand URLs
    print("Getting brand URLs...")
    brands = scrape.get_brand_urls()

    # Get guitar URLs by brand
    print("Getting guitar URLs...")
    scrape.get_guitar_urls(brands)

    # Get guitar data from guitar URLs
    print("Getting guitar data...")
    scrape.get_guitar_data

    # Clean guitar data
    print("Cleaning data...")
    clean.clean_data()
    
    # Push cleaned data to Firestore
    print("Pushing data to Firestore...")
    push.push_data()

run_pipeline()