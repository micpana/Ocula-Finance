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
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import { Symbols } from './lists'
import USD from '../images/usd_flag.png'
import EUR from '../images/eur_flag.png'
import JPY from '../images/jpy_flag.png'
import GBP from '../images/gbp_flag.png'
import CHF from '../images/chf_flag.png'
import ZAR from '../images/zar_flag.png'
import XAU from '../images/xau.png'
import CAD from '../images/cad_flag.png'
import AUD from '../images/aud_flag.png'
import NZD from '../images/nzd_flag.png'
import BTC from '../images/bitcoin.png'
import ETH from '../images/ethereum.png'
import LTC from '../images/lite_coin.png'
import XRP from '../images/xrp.png'
import Modal from './modal';
import { Model_Cards } from './model_cards'

class Analysis extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            network_error_screen: false,
            network_error_message: '',
            retry_function: null,
            input_errors: {},
            on_mobile: false,
            symbol: 'EURUSD',
            market_analysis: [
                {
                    timestamp: '28/08/2024 19:15',
                    entry_timeframe_timestamp: '28/08/2024 19:15',
                    symbol: 'EURUSD',
                    action: 'Buy',
                    stoploss_percentage: -0.75,
                    takeprofit_percentage: 1.5,
                    risk_to_reward_ratio: '1:2',
                    maximum_holding_time: '2 trading hours',
                    trade_close_percentage: 1.5
                }
            ],
            user_subscribed: null,
            user_closing_price_at_entry: null,
            modal_open: false,
            modal_content: null
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});

            // check if value is a symbol, if so load data for selected symbol
            if (Symbols.includes(e.target.value)){
                this.GetCurrentMarketAnalysis(e.target.value)
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

        this.GetCurrentMarketAnalysis = (symbol) => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            var data = new FormData()
            data.append('symbol', symbol)

            axios.post(Backend_Server_Address + 'getMarketAnalysis', data, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set market analysis to state
                this.setState({market_analysis: result})
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
                    }else if (result === 'not subscribed'){
                        this.setState({user_subscribed: false})
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, () => this.GetCurrentMarketAnalysis(symbol))
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, () => this.GetCurrentMarketAnalysis(symbol))
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, () => this.GetCurrentMarketAnalysis(symbol))
                }
                this.LoadingOff()
            })
        }

        this.GetSymbolIcons = (symbol) => {
            var base = ''; var quote = ''
            if(symbol === 'EURUSD'){ base = EUR; quote = USD }
            if(symbol === 'USDJPY'){ base = USD; quote = JPY }
            if(symbol === 'GBPUSD'){ base = GBP; quote = USD }
            if(symbol === 'USDCHF'){ base = USD; quote = CHF }
            if(symbol === 'USDZAR'){ base = USD; quote = ZAR }
            if(symbol === 'XAUUSD'){ base = XAU; quote = USD }
            if(symbol === 'GBPZAR'){ base = GBP; quote = ZAR }
            if(symbol === 'GBPCAD'){ base = GBP; quote = CAD }
            if(symbol === 'GBPAUD'){ base = GBP; quote = AUD }
            if(symbol === 'GBPJPY'){ base = GBP; quote = JPY }
            if(symbol === 'GBPNZD'){ base = GBP; quote = NZD }
            if(symbol === 'NZDCAD'){ base = NZD; quote = CAD }
            if(symbol === 'NZDUSD'){ base = NZD; quote = USD }
            if(symbol === 'AUDNZD'){ base = AUD; quote = NZD }
            if(symbol === 'AUDUSD'){ base = AUD; quote = USD }
            if(symbol === 'AUDCAD'){ base = AUD; quote = CAD }
            if(symbol === 'AUDJPY'){ base = AUD; quote = JPY }
            if(symbol === 'EURNZD'){ base = EUR; quote = NZD }
            if(symbol === 'EURGBP'){ base = EUR; quote = GBP }
            if(symbol === 'EURCAD'){ base = EUR; quote = CAD }
            if(symbol === 'EURAUD'){ base = EUR; quote = AUD }
            if(symbol === 'USDCAD'){ base = USD; quote = CAD }
            if(symbol === 'BTCUSD'){ base = BTC; quote = USD }
            if(symbol === 'ETHUSD'){ base = ETH; quote = USD }
            if(symbol === 'LTCUSD'){ base = LTC; quote = USD }
            if(symbol === 'XRPUSD'){ base = XRP; quote = USD }

            return <Row style={{margin: '0px'}}>
                <Col xs='6'>
                    <img src={base} style={{width: '30px', height: '30px'}} />
                </Col>
                <Col xs='6'>
                    <img src={quote} style={{width: '30px', height: '30px'}} />
                </Col>
            </Row>
        }

        this.OpenModal = (modal_content) => {
            this.setState({modal_content: modal_content, modal_open: true})
        }

        this.CloseModal = () => {
            this.setState({modal_open: false})
        }

        this.ModelCardRender = (symbol) => {
            // symbol's model card
            var symbol_model_card = Model_Cards[symbol]
            // model card render
            return <div>
                <h5>
                    {symbol} AI Model's Performance Card
                </h5>
                <br/>
                <p style={{fontSize: '13px', textAlign: 'left'}}>
                    All test trades were takes using a fixed risk-to-reward ratio and a fixed risk amount in dollars, risking a single dollar to gain two.
                </p>
                <br/><br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Initial account balance:
                    </Col>
                    <Col>
                        ${symbol_model_card["Starting account balance (example in $)"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Account balance after test trades:
                    </Col>
                    <Col>
                        ${symbol_model_card["Account balance after trades ($)"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Number of trades taken:
                    </Col>
                    <Col>
                        {symbol_model_card["Number of trades taken"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Trades won:
                    </Col>
                    <Col>
                        {symbol_model_card["Trades won"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Trades lost:
                    </Col>
                    <Col>
                        {symbol_model_card["Trades lost"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Overall Win Rate:
                    </Col>
                    <Col>
                        {symbol_model_card["Overall Win Rate %"]} %
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Risk:Reward:
                    </Col>
                    <Col>
                        {symbol_model_card["Risk:Reward"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Stoploss Hits:
                    </Col>
                    <Col>
                        {symbol_model_card["Stoploss Hits"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Stoploss Misses:
                    </Col>
                    <Col>
                        {symbol_model_card["Stoploss Misses"]} <span style={{fontSize: '13px'}}>(closed in red but didn't hit the stoploss)</span>
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Takeprofit Misses:
                    </Col>
                    <Col>
                        {symbol_model_card["Takeprofit Misses"]} <span style={{fontSize: '13px'}}>(closed in blue but didn't hit the takeprofit)</span>
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Maximum number of consecutive wins:
                    </Col>
                    <Col>
                        {symbol_model_card["Maximum number of consecutive wins"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Maximum number of consecutive losses:
                    </Col>
                    <Col>
                        {symbol_model_card["Maximum number of consecutive losses"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Average number of consecutive wins:
                    </Col>
                    <Col>
                        {symbol_model_card["Average number of consecutive wins"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Average number of consecutive losses:
                    </Col>
                    <Col>
                        {symbol_model_card["Average number of consecutive losses"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Number of features:
                    </Col>
                    <Col>
                        {symbol_model_card["Number of features"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Training data start date:
                    </Col>
                    <Col>
                        {symbol_model_card["Training data start date"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Training data end date:
                    </Col>
                    <Col>
                        {symbol_model_card["Training data end date"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Training data number of trading days:
                    </Col>
                    <Col>
                        {symbol_model_card["Training data number of trading days"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Test data start date:
                    </Col>
                    <Col>
                        {symbol_model_card["Test data start date"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Test data end date:
                    </Col>
                    <Col>
                        {symbol_model_card["Test data end date"]}
                    </Col>
                </Row>
                <br/>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col style={{fontWeight: 'bold'}}>
                        Test data number of trading days:
                    </Col>
                    <Col>
                        {symbol_model_card["Test data number of trading days"]}
                    </Col>
                </Row>
                <br/>
            </div>
        }

        this.PercentagesToPriceRender = () => {
            // percentages to prices render
            return <div>

            </div>
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // this.GetCurrentMarketAnalysis(this.state.symbol)
    }

    render() {
        // market analysis
        var market_analysis = this.state.market_analysis

        // selected symbol icons
        var selected_symbol_icons = this.GetSymbolIcons(this.state.symbol)
        
        // trade signals / market analysis mapping
        var signals = market_analysis.map((item, index) => {
            // symbol icons
            var symbol_icons = this.GetSymbolIcons(item.symbol)

            // model card modal content
            var model_card_modal_content = this.ModelCardRender(item.symbol)

            // percentages to price modal content
            var percentages_to_price_modal_content = this.PercentagesToPriceRender()

            return <div style={{marginBottom: '15px', border: '1px solid #F2B027', borderRadius: '20px'}}>
                <Row style={{margin: '0px', textAlign: 'left', marginTop: '10px'}}>
                    <Col>
                        <h5>
                            {item.symbol}
                        </h5>
                    </Col>
                    <Col>
                        <a onClick={() => this.OpenModal(model_card_modal_content)} style={{color: 'inherit', cursor: 'pointer'}}>
                            Click here to view the {item.symbol} AI model's performance card.
                        </a>
                    </Col>
                </Row>
                <Row style={{margin: '0px', textAlign: 'left'}}>
                    <Col sm='2'>
                        <br/>
                        {symbol_icons}
                        <br/>
                        <Row style={{margin: '0px'}}>
                            <Col>
                                <h5>
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
                                <h5 style={{color: 'red'}}>
                                    {item.stoploss_percentage} %
                                </h5>
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
                                <h5 style={{color: 'blue'}}>
                                    {item.takeprofit_percentage} %
                                </h5>
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
                                <h5>
                                    {item.risk_to_reward_ratio}
                                </h5>
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
                                <h5>
                                    {item.timestamp}
                                </h5>
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
                                <h5>
                                    {item.maximum_holding_time}
                                </h5>
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
                                    ? <h5>To be updated.</h5>
                                    : <h5 style={{color: item.trade_close_percentage < 0 ? 'red' : 'blue'}}>
                                        {
                                            item.trade_close_percentage
                                        } %
                                    </h5>
                                }
                            </Col>
                        </Row>
                    </Col>
                </Row>
                <h6 style={{textAlign: 'left', marginLeft: '10px', marginTop: '5px', fontSize: '13px'}}>
                    Percentages are % distances from the entry price at the stated entry time. Prices vary according to the broker being used. {' '}
                    <a onClick={() => this.OpenModal(percentages_to_price_modal_content)} style={{color: 'inherit', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold'}}>
                        Click here to convert percentages to prices.
                    </a>
                </h6>
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
                            this.state.user_subscribed === false
                            ? <div>
                                <br/><br/><br/>
                                <h5 style={{color: '#005fc9'}}>You're not subscribed and your free trial expired.</h5>
                                <br/><br/><br/>
                                <Grid width='180px' style={{color: '#005fc9'}}/>
                            </div>
                            : <div>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='3'>
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
                                        <br/>
                                    </Col>
                                    <Col><br/></Col>
                                    <Col sm='2' style={{textAlign: 'right'}}>
                                        {
                                            this.state.symbol == 'ALL'
                                            ? <div></div>
                                            : <div>
                                                {selected_symbol_icons}
                                                <br/>
                                            </div>
                                        }
                                    </Col>
                                </Row>
                                <br/>
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
                                        <Modal isOpen={this.state.modal_open} onClose={this.CloseModal}>
                                            {this.state.modal_content}
                                        </Modal>
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