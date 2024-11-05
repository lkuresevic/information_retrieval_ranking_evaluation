# Data review
**time_epoch** - A timestamp of the event, stated in Unix time.

**device_id** - unique device identifier

**session_id** - unique session identifier (when combined with device_id)

**event_index** - unique identifier of an event within a query, was renamed query_id in code

**experimentGroup** - defines which experiment group the session belongs to, presumably referring to the model which was tested

**queryLenght** - the length of the search query described with the number of characters

**selectedIndexes** - Contains a value of null if no item has been selected within this event in the session (these events always have an 'event_id' of "searchRestarted"), and a list containing a single element referring to the index of the selected item if an item has been selected (these events always have an 'event_id' of "sessionFinished").

**event_id** - Has one of two values; "searchRestarted" if the event within the session ended with the SE window updating (search query edited, additional filters added, etc.) and "sessionFinished" if the event ended with an item being selected (this is the outcome which we considered successful, assuming the user found what they were looking for). It is important to note that data portrays certain sessions ending without an item being selected. This suggests a need for a better data collection mechanism, or at least more specific values for the 'event_id' field, as the current ones offer limited insight.
# Evaluation metrics
placeholder
# Evaluation results
Data collected was rudimentary, but insightful enough for a couple of metrics to be assessed.

Success rate - Using information labeled with 'event_id' and operating under the assumption that only sessions ending with an item being selected (and 'event_id' having a value of "sessionFinished"), we can calculate the percentage of total sessions which ended with the user finding what they were looking for. Sessions from Group 0 had a slightly higher success rate (slightly under a percent), but this superiority is likely statistically insignificant and may be due to relatively small experiment samples.

The faster the user is able to find what they are looking for, the better the model. Average elapsed time before success and average number of queries before success were both straight-forward to calculate, and could be useful metrics to assess the quality of user experience. Although realistically suboptimal, neither model proves significantly better than the other. The same goes for average percentage of change in query length in successful sessions. Perhaps when looking into equivalent metrics in unsuccessful sessions, insight could be gained into which of the models is more likely to have users give up searching for what they need.

When considering ranking of retrieved items which the users actually selected within sessions that ended successfully, we run into the first significant advantage Model 1 demonstrated over Model 0. Once again, the results of both experiment groups are realistically suboptimal, but users from Group 1 found what they were looking for higher up in the search results (ranked at 5.34 on average, as opposed to 6.44), pointing to Model 1 "having a better understanding".

Conclusion:

While neither of the two simulated models appears to perform optimally (low success rate, relatively high search counts and session durations), likely due to still being in early stages of development, they both perform relatively similarly with the exception of Model 1 demonstrating a significant improvement in the ability to rank desired items higher.
