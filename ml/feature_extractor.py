import re
from urllib.parse import urlparse

def extract_url_features(url):
    """
    Takes a URL string and extracts numerical features for ML classification.
    Returns a list of exactly 8 features.
    """
    features = []
    
    # Ensure URL has a scheme (http/https) for accurate parsing by urllib
    if not re.match(r'^https?://', url):
        url = 'http://' + url
        
    try:
        parsed_url = urlparse(url)
    except:
        # If the URL is so malformed it crashes the parser, flag it aggressively
        return [1, 100, 1, 1, 1, 5, 1, 1] 

    domain = parsed_url.netloc

    # Feature 1: Presence of IP Address (1 if True, 0 if False)
    # Regex checks for standard IPv4 format (e.g., 192.168.1.1)
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))'
    )
    features.append(1 if ip_pattern.search(domain) else 0)
    
    # Feature 2: URL Length (Phishing URLs are often very long)
    features.append(len(url))
    
    # Feature 3: URL Shortening Services (e.g., bit.ly, tinyurl)
    shorteners = re.compile(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl')
    features.append(1 if shorteners.search(domain) else 0)
    
    # Feature 4: Presence of '@' Symbol (Used to bypass domain checks)
    features.append(1 if '@' in url else 0)
    
    # Feature 5: Presence of '//' out of place (Redirect mechanism)
    # We check if '//' appears after the initial 'http://' (index 7)
    features.append(1 if url.rfind('//') > 7 else 0)
    
    # Feature 6: Presence of '-' in Domain (Phishers mimic brand names)
    features.append(1 if '-' in domain else 0)
    
    # Feature 7: Number of Dots in the domain (Subdomain abuse)
    features.append(domain.count('.'))
    
    # Feature 8: HTTPS token in the domain part (e.g., http://https-secure-login.com)
    features.append(1 if 'https' in domain else 0)
    
    return features

# Test the function if run directly
if __name__ == "__main__":
    test_url = "http://www.secure-login-paypal.com@192.168.1.1/update"
    print(f"[INFO] Extracting features for: {test_url}")
    print(f"Features Array: {extract_url_features(test_url)}")
    print("Format: [IP, Length, Shortener, '@', '//', Hyphen, Dots, HTTPS_in_domain]")