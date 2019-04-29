from crpapi import CRP, CRPApiError
CRP.apikey = '25bdf6e5f73b10ce7164ce3da1d765f9'

print (CRP.getLegislators.get(id='NJ04'))
