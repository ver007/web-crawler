import os, re, sys, getopt, errno, time, traceback, datetime, string, urlparse, mimetypes, platform
import requests
from bs4 import BeautifulSoup
from functions import mkdir_p, get_filepath, get_encoded_data

from config import urls_to_crawl, file_extensions_list, mimetypes_list, binary_mimetypes_list, request_delay

USAGE_MESSAGE = 'Usage: update_contact_info.py -i <input_file> -o <output_dir>'
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }
LEAF_URL_STRINGS = ['wikipedia.org', 'facebook.com', 'twitter.com', 'last.fm']

def add_contact_info(url, parsed_html):
    
def add_new_urls(url, parsed_html):
    print "Adding new URLs from page source of URL: %s" % url
    for tag in parsed_html.findAll('a', href=True):
        href = tag['href'].strip() # Stripping handles <a href=" http...
        anchor_index = href.find("#") 
        if anchor_index != -1:
            href = href[:anchor_index] # We don't care about anchors
        if href:
            if ignore_query_strings:
                query_string_index = href.find("?") 
                if query_string_index != -1:
                    href = href[:query_string_index]
            href_absolute_url = urlparse.urljoin(url, href)
            if href_absolute_url.startswith('http'): # We don't care about mailto:foo@bar.com etc.
                if follow_links_containing in href_absolute_url and href_absolute_url not in all_urls:
                    urls_to_visit.append(href_absolute_url)
                    all_urls.append(href_absolute_url)
        
def crawl_url():
    global errors_encountered
    print "\n* NEW CRAWLING SESSION FOR CONFIG URL: %s *\n" % seed_url

    while len(urls_to_visit) > 0:
        current_url = urls_to_visit.pop(0)
        try:
            time.sleep(request_delay)
            page_source = None
            met_mimetype_criteria = False
            met_file_extension_criteria = False
            write_file = False
            write_binary = False                                                    
            print "\nProcessing URL: %s\n" % current_url
            # Look for a valid head response from the URL
            print "HEAD Request of URL: ", current_url
            head_response = requests.head(current_url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=60)
            if not head_response.status_code == requests.codes.ok:
                print "Received an invalid HEAD response for URL: ", current_url
            else:
                content_type = head_response.headers.get('content-type')
                encoding = head_response.encoding
                final_url = head_response.url                
                # If we found an HTML file, grab all the links
                if 'text/html' in content_type:
                    print "Requesting URL with Python Requests: ", current_url
                    get_response = requests.get(current_url, headers=REQUEST_HEADERS, timeout=60)
                    content_type = get_response.headers.get('content-type')
                    encoding = get_response.encoding
                    page_source = get_response.text
                    final_url = get_response.url
                    parsed_html = BeautifulSoup(html)
                    add_contact_info(final_url, parsed_html)
                    add_new_urls(final_url, parsed_html)                    

                    
                    url_parsed = urlparse.urlsplit(final_url)
                    url_path = url_parsed.path.strip()


            global files_processed
            files_processed += 1
            print "Files Found: %d  Processed: %d  Remaining: %d  Contact Items Found: %d  Operational Errors: %d" % ( len(all_urls), files_processed, len(urls_to_visit), contact_items_found, errors_encountered )
        except:
            errors_encountered += 1
            try:
                traceback_info = '\n'.join(traceback.format_exception(*(sys.exc_info())))
            except:
                traceback_info = ''
            print "*** ERROR PROCESSING: %s ***\nTraceback: %s\n" % ( current_url, traceback_info )

if __name__ == "__main__":
    argv = sys.argv[1:]
    # Find or create output directory
    output_dir = None
    output_dir = None
    contact_dict
    try:
        opts, args = getopt.getopt(argv, "i:o:" )
    except getopt.GetoptError:
        print USAGE_MESSAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        if opt == "-o":
            output_dir = arg
    if not input_file or not output_dir:
        print USAGE_MESSAGE
        sys.exit(2)
    if os.path.isdir(output_dir):
        print "Found directory: %s" % output_dir
    else:
        mkdir_p(output_dir)
        print "Created directory: %s" % output_dir
    with open(input_file) as f:
        urls = f.readlines()
    print "Found %d URLs" % len(urls)
    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:    
            files_processed = 0
            errors_encountered = 0
            contact_items_found = 0
            urls_to_visit = [url]
            all_urls = [url]

        start_time = datetime.datetime.now()
        print "\nCurrent Time:  %s" % start_time
        crawl_url()
        end_time = datetime.datetime.now()
        print "\nStart:  %s\nFinish: %s\n" % (start_time, end_time)
