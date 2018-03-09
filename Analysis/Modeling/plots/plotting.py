"""Basic plotting with ggplot."""

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from ggplot import *
from dplython import *

# initial data processing
longform_df = DplyFrame(pd.read_csv("../LongForm/longform.csv", dtype={'shorthand_search_vol': int}))
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
p += labs(x="Time", y="Search Volume (Scaled to 100)")
p += ggtitle("Matchweek 1")
p.save('matchweek1.png', width=25, height=10)
