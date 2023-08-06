from __init__ import EventTracker

event_tracker = EventTracker("FhnnD4qPyZEpr0SA2MaFRVxGYTFmRwN7")

print('ue')
resp = event_tracker.track("teste", {}, None, "161cc4a3-baeb-43e6-afc5-bea1f1808a45")
print(resp)
resp2 = event_tracker.identify_user("123abdc", {})
print(resp2)