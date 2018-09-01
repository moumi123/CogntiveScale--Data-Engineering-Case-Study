# CogntiveScale: Data Engineering Case Study

Assumptions:

1. For the first question on Market Cap I have used the link, to get top 100 Market_cap values.
2. In question number 2, the binning I was supposed to do was 0-5,6-11,..... but while checking the data I found out that it has float value, so I did the binning also as follows (0-5],(5-10),.... I took a maximum value as 700.


How to run the files:
1. sector_wise_company.py: It will give all companies sectorwise information and will store it in the table sector_wise_company. (Part of qustion number 1)

2. Market_cap.py : It will give sector wise 3rd and 4th Highest Market Cap value Company's Name (Question Number 1)

3. pe_ratio_details : It will give pe_ratio_details of each and every company as well as per bin, all the companies name. As you mentioned, complete binning,group by thing is done by pandas.
