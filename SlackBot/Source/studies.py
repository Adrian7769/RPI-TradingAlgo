# studies.py
from SlackBot.Source.data import Data

class Studies():
    def __init__():
        data = Data.read_data()
        # THis is where all of the base level data will be for all of your studies to
        # be built off of. This will be the data that is constantly updating in real time.
        # studies need to return data in the correct format so that I can derive other information from them. can I derive 75% expected range used from the expected range?
        pass
    def last_price(self, data):
        value = None
        return value
    # --------------------------------- VALUE -------------------------------- #
    def rth_vpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def eth_vpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def prior_day_vpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def prior_wvpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def prior_mvpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def prior_yvpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    def current_yvpoc(self, data):
        # Access the data and do the calculations needed and return the result
        value = None
        return value
    # --------------------------------- POSTURE ------------------------------ #
    def fd_vpoc(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value    
    def td_vpoc(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def nd_vpoc(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def posture(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def session_posture(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    # ---------------------------------- VWAP -------------------------------- #
    def rth_vwap(self, data):
        # access the data and do the calculations needed and return the result
        # return STD = True then return the standard deviation as well.
        # return SLOPE = True then return the slope of the vwap
        value = None
        return value
    def eth_vwap(self, data):
        # access the data and do the calculations needed and return the result
        # return STD = True then return the standard deviation as well.
        # if false then just return the vwap
        # return SLOPE = True then return the slope of the vwap
        value = None
        return value
    def wvwap(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def mvwap(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def qvwap(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def yvwap(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value    
    def custom_vwap(self, data):
        # Either Pass in a date and time or pass in a Study like current day high.
        value = None
        return value
    # ------------------------------ MARKET LEVELS --------------------------- # 
    def session_levels(self, data):
        # access the data and do the calculations for any given session or sessions.
        day_high = None
        day_low = None
        day_open = None
        day_close = None
        day_mid = None
        return day_high, day_low, day_open, day_close, day_mid
    def opening_range(self, data):
        # access the data and do the calculations needed and return the result
        or_high = None
        or_low = None 
        return or_high, or_low, 
    def prior_week_levels(self, data):
        # access the data and do the calculations needed and return the result
        week_high = None
        week_low = None
        week_open = None
        week_close = None
        week_mid = None
        return week_high, week_low, week_open, week_close, week_mid
    def prior_month_levels(self, data):
        # access the data and do the calculations needed and return the result
        month_high = None
        month_low = None
        month_open = None
        month_close = None
        month_mid = None
        return month_high, month_low, month_open, month_close, month_mid
    def prior_year_levels(self, data):
        # access the data and do the calculations needed and return the result
        year_high = None
        year_low = None
        year_open = None
        year_close = None
        year_mid = None
        return year_high, year_low, year_open, year_close, year_mid
    def custom_levels(self, data):
        # Pass in the custom time range and return the custom results
        custom_high = None
        custom_low = None
        custom_open = None
        custom_close = None
        custom_mid = None
        return custom_high, custom_low, custom_open, custom_close
    # ------------------------------ ORDERFLOW ----------------------------- #
    def relative_volume(self, data):
        # access the data and do the calculations needed and return the result
        # find out the capabilitys of the API and perhaps figure out how to calculate
        # 30 minute relative volume?
        value = None
        return value
    def delta(self, data):
        # Pass in the period of time you want to calculate the delta for and return the result
        # Use this to calculate the OVN delta as well as RTH delta.
        value = None
        return value
    # --------------------------- MARKET PROFILE ---------------------------- #
    def period(self, data):
        # pass in the period letter or the range of period letters that you want, return the open, high, low, close, and mid
        value = None
        return value
    def open_type(self, data):
        # return the open type for the current period or any given period.
        value = None
        return value
    def day_type(self, data):
        # return the day type for the current day or any given period
        value = None
        return value
    def composite(self, data):
        # pass in the period letter or the range of period letters that you want, return the open, high, low, close, and mid
        value = None
        return value
    def initial_balance(self, data):
        # return the initial balance high, low, 0.5x, 1x, 1.5x, 2x.
        value = None
        return value
    def t_vpoc(self, data):
        # access the data and do the calculations needed and return the result
        value = None
        return value
    def single_print_past(self, data):
        # return all of the single prints for the last x amount of time.
        value = None
        return value
    def single_print_current(self, data):
        # return all of the single prints for the current period.
        value = None
        return value
    def excess(self, data):
        # return all of the excess for the given period.
        value = None
        return value
    # --------------------------- VOLUME PROFILE ---------------------------- #
    def composite(self, data):
       # return the composte profile for given time range.
        value = None
        return value
    def structure(self, data):
        # would it be possible to format the profile and then classify its shape into a structure? Balanced, Trending, Etc? 
        # and could you do this for any given period of time?? DVPOC ALIGNS WITH COMPOSITE NODE THAT COULD BECOME 5DA
        # How can you tell if a vpoc is prominant???? or NOT???
        value = None
        return value
    def naked_vpoc(self, data):
        # return all of the naked vpocs for the last x amount of time.
        value = None
        return value
    def value_area(self,data):
        # return the value area high, low, and point of control.
        value = None
        return value
    # ------------------------------- ECONOMIC ------------------------------ #
    def economic_scene(self, data):
        # return all of the economic events for the current day.
        value = None
        return value
    # ------------------------------ STATISTICS ----------------------------- #
    # perhaps run these on the init process to save on runtime latensy?
    def ib_atr(self, data):
        # return the IB ATR
        value = None
        return value
    # ------------------------------ OVERNIGHT ------------------------------ #
    def ovn(self, data):
        # return the overnight high, low.
        value = None
        return value
    def euro(self, data):
        # return the euro high, low.
        value = None
        return value
    # ------------------------------ DERRIVATIVES ---------------------------- #
    def iv(self, data):
        # return the implied volatility
        value = None
        return value
    def expected_range(self, data):
        # return the expected range, expected high, expected low for a given period of time.
        value = None
        return value
    
    
    
    
        