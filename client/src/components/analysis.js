import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Helmet } from 'react-helmet'
import {
    Audio,
    BallTriangle,
    Bars,
    Circles,
    Grid,
    Hearts,
    Oval,
    Puff,
    Rings,
    SpinningCircles,
    TailSpin,
    ThreeDots,
} from '@agney/react-loading';
import { ToastContainer, toast } from 'react-toastify';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import NotificationAlert from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import { Symbols } from './lists'
import Modal from './modal';
import { Model_Cards } from './model_cards'
import ModelCardRender from './model_card_render'
import SymbolIconsRender from './symbol_icons_render';
import DateTimeDisplay from './timezone_conversion'
import { FaMonero, FaMoneyBillWave } from 'react-icons/fa';

class Analysis extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: true,
            network_error_screen: false,
            network_error_message: '',
            retry_function: null,
            input_errors: {},
            end_of_list: false,
            on_mobile: false,
            queried_symbol: 'ALL',
            symbol: 'ALL',
            market_analysis: [],
            user_subscribed: null,
            telegram_verified: null,
            telegram_connect_code: null,
            user_closing_price_at_entry: null,
            modal_open: false,
            modal_selection: null,
            selected_signal: {},
            user_device_time: null, 
            user_device_timezone: null,
            user_time_by_id_address: null, 
            user_timezone_by_id_address: null,
            notification_permission_granted: false,
            initial_request: true
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});

            // check if value is a symbol, or ALL, if so load data for selected symbol
            if (Symbols.includes(e.target.value) || e.target.value === 'ALL'){
                this.GetCurrentMarketAnalysis(e.target.value, false, true, true)
            }
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // existing errors
            var existing_errors = this.state.input_errors

            // existing errors modified
            existing_errors[field] = error

            // update state
            this.setState({input_errors: existing_errors})
        }

        this.ClearInputErrors = () => {
            // existing errors
            var existing_errors = this.state.input_errors
            // array of existing error field names
            var existing_error_fields = Object.keys(existing_errors)
            // set existing error fields to undefined, clearing them
            existing_error_fields.map((item, index) => {
                existing_errors[item] = undefined
            })
            this.setState({input_errors: existing_errors})
        }

        this.LoadingOn = () => {
            this.setState({loading: true})
        }

        this.LoadingOff = () => {
            this.setState({loading: false})
        }

        this.NetworkErrorScreenOn = (error_message, retry_function) => {
            this.setState({network_error_screen: true, network_error_message: error_message, retry_function: retry_function})
        }

        this.NetworkErrorScreenOff = () => {
            this.setState({network_error_screen: false, network_error_message: '', retry_function: null})
        }

        this.GetCurrentMarketAnalysis = (symbol, get_all, bypass_time_check, show_loading_screen) => {
            // get current minutes from time
            const now = new Date();
            const current_minutes = String(now.getMinutes());

            // if there's a time check bypass or the current minutes represent a 15 minute candle close, ie 00, 15, 30, 45
            if (
                (bypass_time_check === true) ||
                (
                    (current_minutes === '00') ||
                    (current_minutes === '15') ||
                    (current_minutes === '30') ||
                    (current_minutes === '45')
                )
            ){
                const { cookies } = this.props;
                if (show_loading_screen == true){
                    this.LoadingOn()
                }
                this.NetworkErrorScreenOff()

                if (symbol != this.state.queried_symbol){ // current selected symbol is not the one that one previously queried
                    var length_of_data_received = 0
                    var clear_market_analysis_state_first = true
                }else{ // same symbol selection
                    var length_of_data_received = this.state.market_analysis.length
                    var clear_market_analysis_state_first = false
                }

                var data = new FormData()
                data.append('symbol', symbol)
                data.append('length_of_data_received', length_of_data_received)
                data.append('get_all', get_all) // bool
                // timestamp and symbol of the most recent trade signal received
                if (this.state.market_analysis.length > 0 && symbol == 'ALL'){
                    data.append('timestamp_of_most_recent_signal_received', this.state.market_analysis[0].timestamp)
                    data.append('symbol_of_most_recent_signal_received', this.state.market_analysis[0].symbol)
                }else if (this.state.market_analysis.filter(item => item.symbol === symbol).length > 0){
                    data.append('timestamp_of_most_recent_signal_received', this.state.market_analysis.filter(item => item.symbol === symbol)[0].timestamp)
                    data.append('symbol_of_most_recent_signal_received', symbol)
                }else{
                    data.append('timestamp_of_most_recent_signal_received', '')
                    data.append('symbol_of_most_recent_signal_received', '')
                }

                axios.post(Backend_Server_Address + 'getMarketAnalysis', data, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // set end of list to false
                    this.setState({end_of_list: false})
                    // if we're clearing the current market_analysis state first
                    if(clear_market_analysis_state_first == true){
                        var market_analysis = []
                    }else{
                        var market_analysis = this.state.market_analysis
                    }
                    if (get_all == true){
                        // set market analysis to state
                        this.setState({market_analysis: result})
                    }else{
                        // add market analysis to state ... all arrays have the syntax = newer data first ... so append existing data to new data to respect the existing order
                        this.setState({market_analysis: result.concat(market_analysis)})

                        // trade signal(s) browser notification ... only if this is not the initial request and this is a function recall for the same symbol
                        if (this.state.initial_request === false && symbol == this.state.queried_symbol){
                            this.ShowTradeSignalsNotification(result)
                        }

                        // set initial request to false ... only if its current set to true
                        if (this.state.initial_request === true){
                            this.setState({initial_request: false})
                        }
                    }
                    // update queried_symbol to symbol
                    this.setState({queried_symbol: symbol})
                    this.LoadingOff()
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(
                            result === 'access token disabled via signout' ||
                            result === 'access token expired' ||
                            result === 'not authorized to access this' ||
                            result === 'invalid token'
                        ){ 
                            // delete token from user cookies
                            cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                            // redirect to sign in
                            let port = (window.location.port ? ':' + window.location.port : '');
                            window.location.href = '//' + window.location.hostname + port + '/signin';
                        }else if(result === 'end of list'){
                            this.setState({end_of_list: true})
                        }else if(result === 'invalid length of data received'){
                            notification_message = 'Invalid length of data received'
                            NotificationAlert(notification_message, 'error')
                            this.NetworkErrorScreenOn(notification_message, () => this.GetUserPastPayments(get_all))
                        }else if (result === 'not subscribed'){
                            this.setState({user_subscribed: false})
                        }else if (result === 'telegram not verified'){
                            this.setState({telegram_verified: false})
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            // NotificationAlert(notification_message, 'error')
                            // this.NetworkErrorScreenOn(notification_message, () => this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen))
                            this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen)
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        // NotificationAlert(Network_Error_Message, 'error')
                        // this.NetworkErrorScreenOn(Network_Error_Message, () => this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen))
                        this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen)
                    }else{ // error occured during request setup ... no network access
                        // NotificationAlert(No_Network_Access_Message, 'error')
                        // this.NetworkErrorScreenOn(No_Network_Access_Message, () => this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen))
                        this.GetCurrentMarketAnalysis(symbol, get_all, true, show_loading_screen)
                    }
                    this.LoadingOff()
                })
            }
        }

        this.OpenModal = (modal_selection) => {
            this.setState({modal_selection: modal_selection, modal_open: true})
        }

        this.CloseModal = () => {
            this.setState({modal_open: false, user_closing_price_at_entry: null})
        }

        this.PercentagesToPriceRender = () => {
            // selected signal
            var selected_signal = this.state.selected_signal
            
            // symbol
            var symbol = selected_signal.symbol

            // action
            var action = selected_signal.action

            // timestamp
            var timestamp = selected_signal.timestamp

            // stoploss percentage
            var stoploss_percentage = selected_signal.stoploss_percentage

            // takeprofit percentage
            var takeprofit_percentage = selected_signal.takeprofit_percentage

            // trade close percentage
            var trade_close_percentage = selected_signal.trade_close_percentage

            // user's closing price at entry
            var user_closing_price_at_entry = this.state.user_closing_price_at_entry

            // stoploss percentage to stoploss price
            if (user_closing_price_at_entry == null || isNaN(user_closing_price_at_entry) == true || user_closing_price_at_entry == 0){
                var stoploss_price = 'Awaiting entry price input.'
            }else{
                var stoploss_price = parseFloat(user_closing_price_at_entry) + ((parseFloat(stoploss_percentage) / 100) * parseFloat(user_closing_price_at_entry))
            }

            // takeprofit percentage to takeprofit price
            if (user_closing_price_at_entry == null || isNaN(user_closing_price_at_entry) == true || user_closing_price_at_entry == 0){
                var takeprofit_price = 'Awaiting entry price input.'
            }else{
                var takeprofit_price = parseFloat(user_closing_price_at_entry) + ((parseFloat(takeprofit_percentage) / 100) * parseFloat(user_closing_price_at_entry))
            }

            // trade close percentage to trade close price
            if (trade_close_percentage == null || trade_close_percentage == undefined){
                var trade_close_price = 'To be updated.'
            }else{
                if (user_closing_price_at_entry == null || isNaN(user_closing_price_at_entry) == true || user_closing_price_at_entry == 0){
                    var trade_close_price = 'Awaiting entry price input.'
                }else{
                    var trade_close_price = parseFloat(user_closing_price_at_entry) + ((parseFloat(trade_close_percentage) / 100) * parseFloat(user_closing_price_at_entry))
                }
            }

            // percentages to prices render
            return <div>
                <h5>
                    {symbol} Percentages to Prices Conversion
                </h5>
                <div style={{width: '100%', borderBottom: '1px solid #F9C961'}}></div>
                <div style={{textAlign: 'left', fontSize: '13px', marginTop: '10px', fontWeight: 'bold'}}>
                    <span style={{color: action === 'Buy' ? 'blue' : 'red'}}>
                        {action}  Trade
                    </span>
                </div>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}} sm='3'>
                        Entry time:
                        <br/>
                    </Col>
                    <Col>
                        <span style={{fontSize: '13px'}}>
                            <DateTimeDisplay datetimeString={timestamp} /> {this.state.user_device_timezone} Timezone 
                            (matches your device clock, therefore all timestamps inside the dashboard are being displayed in your 
                            local time. <span style={{fontWeight: 'bold'}}>Your broker's timezone maybe different from yours.</span>)
                        </span>
                        <br/>
                    </Col>
                </Row>
                <Label style={{textAlign: 'left'}}>Enter your broker's closing price at the stated entry time <span style={{color: 'red'}}>*</span></Label>
                <InputGroup>
                    <InputGroupText addonType="prepend">
                        <FaMoneyBillWave style={{margin:'10px'}}/>
                    </InputGroupText>
                    <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                        placeholder="Use the 15 minute timeframe and below" name="user_closing_price_at_entry" id="user_closing_price_at_entry"
                        value={this.state.user_closing_price_at_entry} onChange={this.HandleChange} type="number" 
                    />
                </InputGroup>
                <br/><br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Takeprofit Price:
                    </Col>
                    <Col>
                        {takeprofit_price}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Stoploss Price:
                    </Col>
                    <Col>
                        {stoploss_price}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Trade Closed At:
                    </Col>
                    <Col>
                        {trade_close_price}
                    </Col>
                </Row>
                <br/>
            </div>
        }

        this.GetTelegramConnectCode = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getTelegramConnectCode', null, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set telegram connect code to state
                this.setState({telegram_connect_code: result.telegram_connect_code})
                this.LoadingOff()
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'access token disabled via signout' ||
                        result === 'access token expired' ||
                        result === 'not authorized to access this' ||
                        result === 'invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        NotificationAlert(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, this.GetTelegramConnectCode)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    NotificationAlert(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetTelegramConnectCode)
                }else{ // error occured during request setup ... no network access
                    NotificationAlert(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetTelegramConnectCode)
                }
                this.LoadingOff()
            })
        }

        this.VerifyTelegramConnection = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'verifyTelegramConnection', null, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // get telegram connection status
                let telegram_connected = result.telegram_connected
                // if connection was a success, reload GetCurrentMarketAnalysis function, set telegram_verified state to true
                if (telegram_connected == true){
                    this.GetCurrentMarketAnalysis(this.state.symbol, false, true, true)
                    this.setState({telegram_verified: true})
                    NotificationAlert('Telegram verification successful.', 'success')
                }else{
                    // if connection was not a success, notify the user
                    NotificationAlert('The Telegram connection could not be verified. Please verify that you sent the correct code to our bot and try again.', 'error')
                }
                this.LoadingOff()
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'access token disabled via signout' ||
                        result === 'access token expired' ||
                        result === 'not authorized to access this' ||
                        result === 'invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else if(result === 'telegram id has already been used on another account'){
                        NotificationAlert('The Telegram account you used has already been linked to another account on this platform.', 'error')
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        NotificationAlert(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, this.VerifyTelegramConnection)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    NotificationAlert(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.VerifyTelegramConnection)
                }else{ // error occured during request setup ... no network access
                    NotificationAlert(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.VerifyTelegramConnection)
                }
                this.LoadingOff()
            })
        }

        // function to get the user's time and timezone using their device's close
        this.GetUserTimeByDeviceClock = () => {
            // get the device's time
            const now = new Date();
            const formatted_datetime = now.toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',  // Use '2-digit' for numerical month (01, 02, etc.)
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false // Change to false for 24-hour format
            });
            // get the device's timezone
            const device_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            
            // set time data to state
            this.setState({user_device_time: formatted_datetime, user_device_timezone: device_timezone})
        }

        // function to fetch the current date and time based on the user's IP
        this.GetUserTimeByIpAddress = async () => {
            try {
                // fetching data from the WorldTimeAPI
                const response = await fetch('https://worldtimeapi.org/api/ip');
                const data = await response.json();
                
                // extracting the datetime and timezone info from the response
                const userDateTime = data.datetime;  // The date and time in ISO 8601 format
                const userTimezone = data.timezone;  // The user's timezone
                
                // set time data to state
                this.setState({user_time_by_id_address: userDateTime, user_timezone_by_id_address: userTimezone})
            } catch (error) {
                console.error('Error fetching time:', error);
            }
        }

        // check if the user has granted us permission to show notifications
        this.CheckIfNotificationPermissionsAreGranted = () => {
            if (Notification.permission === "granted"){ // default (user has not been asked yet), granted, denied
                this.setState({notification_permission_granted: true})
            }else{
                this.setState({notification_permission_granted: false})
            }
        }

        // request permission to show notifications
        this.RequestNotificationPermission = () => {
            Notification.requestPermission((result) => {
                if (result === 'granted'){ // granted, denied, default (user decision is unknown)
                    this.setState({notification_permission_granted: true})
                }
            });              
        }

        this.ShowTradeSignalsNotification = (new_signals) => {
            if (this.state.notification_permission_granted === true && new_signals.length > 0){
                const img = '/favicon.png'; // notification icon ... public folder is the root folder and the favicon is located inside it
                const title = 'New Trading Signals Available | Ocula Finance' // notification title
                let text = new_signals.map(item => `${item.action} ${item.symbol}`).join(', '); // notification body
                const notification = new Notification(title, {body: text, icon: img, tag: 'new_signals_alert'});
            }
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // get user device's datetime data, and run the function every 3 seconds
        setInterval(this.GetUserTimeByDeviceClock, 3000);
        // get user ip address' datetime data, and run the function every 3 seconds
        // setInterval(this.GetUserTimeByIpAddress, 3000);
        // check if the user has granted us permission to show notifications
        this.CheckIfNotificationPermissionsAreGranted()
        // initial request for market analysis data
        this.GetCurrentMarketAnalysis(this.state.symbol, false, true, true)
        // run the market analysis retrieval function every 3 seconds
        setInterval(() => this.GetCurrentMarketAnalysis(this.state.symbol, false, false, false), 3000);
    }

    render() {
        // market analysis
        var market_analysis = this.state.market_analysis

        // trade signals / market analysis mapping
        var signals = market_analysis.map((item, index) => {
            return <div
                style={{marginBottom: '15px', border: '1px solid #F2B027', borderRadius: '20px'}}
            >
                <Row style={{margin: '0px', textAlign: 'left', marginTop: '10px'}}>
                    <Col>
                        <h5>
                            {item.symbol}
                        </h5>
                    </Col>
                    <Col>
                        <a onClick={() => this.OpenModal('model_card')} 
                            style={{color: 'inherit', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold'}}
                        >
                            Click here to view the {item.symbol} AI model's performance card.
                        </a>
                    </Col>
                </Row>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col sm='2'>
                        <br/>
                        <SymbolIconsRender symbol={item.symbol} />
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h5 style={{color: item.action === 'Buy' ? 'blue' : 'red'}}>
                                    {item.action}
                                </h5>
                            </Col>
                        </Row>
                    </Col>
                    <Col>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Stoploss Percentage:
                                </h6>
                            </Col>
                            <Col>
                                <h6 style={{color: 'red'}}>
                                    {item.stoploss_percentage} %
                                </h6>
                            </Col>
                        </Row>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Takeprofit Percentage:
                                </h6>
                            </Col>
                            <Col>
                                <h6 style={{color: 'blue'}}>
                                    {item.takeprofit_percentage} %
                                </h6>
                            </Col>
                        </Row>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Risk to reward ratio:
                                </h6>
                            </Col>
                            <Col>
                                <h6>
                                    {item.risk_to_reward_ratio}
                                </h6>
                            </Col>
                        </Row>
                    </Col>
                    <Col>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Entry time:
                                </h6>
                            </Col>
                            <Col>
                                <h6>
                                    <DateTimeDisplay datetimeString={item.timestamp} />
                                </h6>
                            </Col>
                        </Row>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Maximum Holding Time:
                                </h6>
                            </Col>
                            <Col>
                                <h6>
                                    {item.maximum_holding_time}
                                </h6>
                            </Col>
                        </Row>
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h6>
                                    Trade Closed At:
                                </h6>
                            </Col>
                            <Col>
                                {
                                    item.trade_close_percentage == null || item.trade_close_percentage == undefined
                                    ? <h6>To be updated.</h6>
                                    : <h6 style={{color: item.action === 'Buy' ? item.trade_close_percentage < 0 ? 'red' : 'blue' : item.trade_close_percentage < 0 ? 'blue' : 'red'}}>
                                        {
                                            item.trade_close_percentage
                                        } %
                                    </h6>
                                }
                            </Col>
                        </Row>
                    </Col>
                </Row>
                <h6 style={{textAlign: 'left', marginLeft: '10px', marginTop: '15px', fontSize: '13px'}}>
                    Percentages are % distances from the entry price at the stated entry time. Prices vary according to the broker being used. {' '}
                    <a onClick={() => {this.setState({selected_signal: item});this.OpenModal('percentages_to_price')}} style={{color: 'inherit', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold'}}>
                        Click here to convert percentages to prices.
                    </a>
                    <br/>
                    Chart timezones also vary according to the broker being used, keep that in mind when backtesting or just scrolling back to find an old entry.
                    <br/>
                    Utilize an appropriate lot size to maintain effective risk management practices.
                </h6>
                <Modal isOpen={this.state.modal_open} onClose={this.CloseModal} handleChange={this.HandleChange}>
                    {
                        this.state.modal_selection === 'model_card'
                        ? <ModelCardRender symbol={item.symbol} />
                        : <div>
                            {
                                this.state.modal_selection === 'percentages_to_price'
                                ? <this.PercentagesToPriceRender />
                                : null
                            }
                        </div>
                    }
                </Modal>
            </div>
        })


        return (
            <div>
                <Helmet>
                    <title>Market Analysis | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            Analysis
                        </h5>
                        <br/><br/>
                        {
                            this.state.telegram_verified === false
                            ? <div>
                                <h6 style={{color: '#005fc9'}}>
                                    Please follow the steps below to connect your Telegram account and start your free trial. {' '}
                                    <Grid width='20px' style={{color: '#005fc9'}}/>
                                </h6>
                                <br/><br/>
                                <ol>
                                    <li>
                                        <h6 style={{textAlign: 'left', fontWeight: 'bold'}}>
                                            Get your Telegram connect code using the button below:
                                        </h6>
                                        <br/>
                                        {
                                            this.state.telegram_connect_code === null
                                            ? <div style={{textAlign: 'left'}}>
                                                <Button onClick={this.GetTelegramConnectCode} 
                                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                                >
                                                    Get code
                                                </Button>
                                            </div>
                                            : <div style={{textAlign: 'left'}}>
                                                Your Telegram connect code is: <span style={{fontWeight: 'bold'}}>
                                                    {this.state.telegram_connect_code}
                                                </span>
                                            </div>
                                        }
                                    </li>
                                    <br/><br/>
                                    <li>
                                        <h6 style={{textAlign: 'left', fontWeight: 'bold'}}>
                                            Send the code to our Telegram bot using any of the options below:
                                        </h6>
                                        <br/>
                                        <p style={{textAlign: 'justify'}}>
                                            Click on the following link: <a href='https://t.me/OculaFinanceBot' target='_blank' style={{color: 'inherit'}}>
                                                https://t.me/OculaFinanceBot
                                            </a>, once you're inside the chat, click on the start button, then send the telegram connect code 
                                            you've received above.
                                            <br/><br/>
                                            Alternatively, you can open your Telegram app, head on to the search bar, and type in <span style={{fontWeight: 'bold'}}> 
                                                oculafinance
                                            </span>. On the search results, click on <span style={{fontWeight: 'bold'}}>
                                                Ocula Finance Bot
                                            </span>. Once you're inside the chat, click on the start button, then send the telegram connect code 
                                            you received above.
                                        </p>
                                    </li>
                                    <br/><br/>
                                    <li>
                                        <h6 style={{textAlign: 'left', fontWeight: 'bold'}}>
                                            Verify your Telegram connection using the button below:
                                        </h6>
                                        <br/>
                                        <div style={{textAlign: 'left'}}>
                                            <Button onClick={this.VerifyTelegramConnection} 
                                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Verify connection
                                            </Button>
                                        </div>
                                    </li>
                                </ol>
                            </div>
                            : this.state.user_subscribed === false
                            ? <div>
                                <br/><br/><br/>
                                <h5 style={{color: '#005fc9'}}>You're not subscribed and your free trial expired.</h5>
                                <br/><br/><br/>
                                <Grid width='180px' style={{color: '#005fc9'}}/>
                            </div>
                            : <div>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='2'>
                                        <Label style={{fontWeight: 'bold'}}>Symbol:</Label>
                                        <select name='symbol' value={this.state.symbol} onChange={this.HandleChange}
                                            style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                        >
                                            <option value='ALL'>ALL</option>
                                            {
                                                Symbols.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                        <br/><br/>
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontSize: '13px'}}>
                                            {this.state.user_device_time} {this.state.user_device_timezone} Timezone 
                                            (matches your device clock, therefore all timestamps inside the dashboard are being displayed in your 
                                            local time. <span style={{fontWeight: 'bold'}}>Your broker's timezone maybe different from yours.</span>)
                                        </span>
                                        <br/><br/>
                                    </Col>
                                    <Col sm='2' style={{textAlign: 'right'}}>
                                        {
                                            this.state.symbol == 'ALL'
                                            ? <div><br/></div>
                                            : <div>
                                                <SymbolIconsRender symbol={this.state.symbol} />
                                                <br/><br/>
                                            </div>
                                        }
                                    </Col>
                                </Row>
                                {
                                    this.state.notification_permission_granted === false
                                    ? <div style={{fontSize: '13px', textAlign: 'justify'}}>
                                        If you wish to turn on browser notifications for our AI's trade signal alerts,
                                        <span onClick={this.RequestNotificationPermission}
                                            style={{fontWeight: 'bold', cursor: 'pointer'}}
                                        >
                                            {' '}click here
                                        </span>.
                                        <br/><br/>
                                    </div>
                                    : <></>
                                }
                                {
                                    market_analysis.length === 0
                                    ? <div>
                                        <h5 style={{color: '#005fc9'}}>
                                            Trade entries found by our AI will appear here
                                        </h5>
                                        <br/>
                                        <Circles width='180px' style={{color: '#005fc9'}}/>
                                    </div>
                                    : <div>
                                        {signals}
                                        <br/>
                                        {
                                            this.state.end_of_list === true
                                            ? <p style={{color: '#00539C', fontWeight: 'bold'}}>All data loaded</p>
                                            : <></>
                                        }
                                        <br/>
                                        <Button onClick={() => {this.GetCurrentMarketAnalysis(this.state.symbol, false, true, true); this.setState({end_of_list: false})}} 
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                        >
                                            Load more
                                        </Button>
                                        {/* {' '}
                                        <Button onClick={() => {this.GetCurrentMarketAnalysis(this.state.symbol, true); this.setState({end_of_list: false})}} 
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                        >
                                            Load all
                                        </Button> */}
                                        <br/><br/>
                                    </div>
                                }
                            </div>
                        }
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Analysis);