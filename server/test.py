import dns.resolver

domain = "oculafinance.com"
record_types = ["A", "CNAME", "MX", "TXT", "NS"]

for record_type in record_types:
    try:
        answers = dns.resolver.resolve(domain, record_type)
        print(f"{record_type} Records:")
        for answer in answers:
            print(answer)
    except Exception as e:
        print(f"Error fetching {record_type}: {e}")
