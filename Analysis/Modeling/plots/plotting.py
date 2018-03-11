"""Basic plotting with ggplot."""

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from ggplot import *
from dplython import *

# initial data processing
longform_df = DplyFrame(pd.read_csv("../../LongForm/longform.csv", dtype={'shorthand_search_vol': int}))
longform_df["date"] = longform_df.match_id.apply(lambda x: "20" + x.split("20")[-1])
longform_df['date_time'] = longform_df['date'].astype(str) + " " + longform_df['time'].astype(str)
longform_df['date_time'] = pd.to_datetime(longform_df['date_time'], errors="coerce", infer_datetime_format=True)

# filtering with dplyr
longform_df >> sift(X.match_wk == 0)


# plot matchweek 1
p = ggplot(aes(x='date_time',
               y='shorthand_search_vol',
               group="match_id",
               color="match_id"),
           data=longform_df >> sift(X.match_wk == 0))

p += geom_line()
p += scale_x_date(labels=date_format("%H:%M:%S"), date_breaks="1 hour")
p += facet_grid('date', scales='free_x')
p += labs(x="Time (GMT)", y="Search Volume (Scaled to 100)")
p += ggtitle("EPL Matchweek 1, 2015/2016")
p.save('matchweek1.png', width=25, height=10)


# plotting an individual match (w/ match events!)
p = ggplot(aes(x='date_time',
               y='shorthand_search_vol',
               group="match_id",
               color="match_id"),
           data=longform_df >> sift((X.match_id == "chelsea2015-08-16") |
                                    (X.match_id == "manchester_city2015-08-16")))
p += geom_line()
p += labs(x="time (gmt)", y="search volume (scaled to 100)")
p += ggtitle("man. city (h) vs. chelsea (a), aug. 8 '16, etihad stadium")

# add in shaded rectangle to indicate actual match TODO
# rect_df = longform_df >> sift(X.stage_2_ind == 1) >> \
#                          sift(X.match_id == "chelsea2015-08-16")
#
# p += geom_rect(df, aes(xmin="start", xmax="end", ymin=0, ymax=100))

# add in lines for home & away goals
# filtered_df = longform_df >> sift(X.home_goal == 1) >> \
#                              sift(X.match_id == "chelsea2015-08-16")
#
# for index, row in filtered_df.iterrows():
#     p += geom_vline(xintercept=[row["date_time"]], color='red')

p += scale_x_date(labels=date_format("%H:%M:%S"), date_breaks="30 minutes")
p.save('chelsea_manchester_city2015-08-16.png', width=25, height=10)

# use the below to inform assumptions about ARIMA parameters

# let's only plot stage 2 of that match
stage_2_df = longform_df >> sift(X.stage_2_ind == 1) \
                         >> sift((X.match_id == "chelsea2015-08-16") |
                                 (X.match_id == "manchester_city2015-08-16"))

p = ggplot(aes(x='date_time',
               y='shorthand_search_vol',
               group="match_id",
               color="match_id"),
           data=stage_2_df)

p += geom_line()
p += scale_x_date(labels=date_format("%H:%M:%S"), date_breaks="1 hour")
p += labs(x="time (gmt)", y="search volume (scaled to 100)")
p += ggtitle("[match only] man. city (h) vs. chelsea (a), aug. 8 '16, etihad stadium")
p.save('chelsea_manchester_city2015-08-16_stage_2.png', width=25, height=10)

# and now let's plot the "stationarized" version (first difference)
stage_2_df["first_diff"] = stage_2_df.shorthand_search_vol.diff(periods=1)
p = ggplot(aes(x='date_time',
               y='first_diff',
               group="match_id",
               color="match_id"),
           data=stage_2_df)

p += geom_line()
p += scale_x_date(labels=date_format("%H:%M:%S"), date_breaks="1 hour")
p += labs(x="time (gmt)", y="+/- differences in search volume (per 8 minutes)")
p += geom_hline(y=0, color='BurlyWood')
p += ggtitle("[Stationarized] man. city (h) vs. chelsea (a), aug. 8 '16, etihad stadium")
p.save('chelsea_manchester_city2015-08-16_stationarized.png', width=25, height=10)
