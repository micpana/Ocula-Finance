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
            current_market_analysis: {},
            user_subscribed: null,
            user_last_m15_close: null
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

            axios.post(Backend_Server_Address + 'getCurrentMarketAnalysis', data, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set current market analysis to state
                this.setState({current_market_analysis: result})
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

        this.GetSymbolIcons = () => {
            var symbol = this.state.symbol
            var base = ''
            var quote = ''
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
                    <img src={base} style={{width: '50px', height: '50px'}} />
                </Col>
                <Col xs='6'>
                    <img src={quote} style={{width: '50px', height: '50px'}} />
                </Col>
            </Row>
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        this.GetCurrentMarketAnalysis(this.state.symbol)
    }

    render() {
        // market analysis
        var current_market_analysis = this.state.current_market_analysis
        var maximum_possible_up_move = current_market_analysis.maximum_possible_up_move
        var maximum_possible_down_move = current_market_analysis.maximum_possible_down_move

        // risk to reward ... risk = 1
        var up_reward = Math.round((maximum_possible_up_move/maximum_possible_down_move) * 1000) / 1000
        var down_reward = Math.round((maximum_possible_down_move/maximum_possible_up_move) * 1000) / 1000

        // price based analysis
        var user_last_m15_close = this.state.user_last_m15_close
        var up_move_possible_maximum_price = user_last_m15_close - -1 * ((maximum_possible_up_move / 100) * user_last_m15_close)
        var down_move_possible_maximum_price = user_last_m15_close - ((maximum_possible_down_move / 100) * user_last_m15_close)

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
                                            {
                                                Symbols.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                        <br/>
                                    </Col>
                                    <Col><br/></Col>
                                    <Col sm='4' style={{textAlign: 'right'}}>
                                        <this.GetSymbolIcons/>
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <h6 style={{fontWeight: 'bold', textAlign: 'left'}}>
                                    Last updated: <span style={{color: '#005fc9'}}>{current_market_analysis.timestamp}</span>
                                </h6>
                                <br/>
                                <h6 style={{textAlign: 'left', fontWeight: 'bold'}}>
                                    Predictions for the next 105 minutes (seven 15 minute candles)
                                </h6>
                                <br/><br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <Row>
                                            <Col sm='6'>
                                                <Container>
                                                    <div style={{backgroundColor: 'green', height: '150px', width: '150px', borderRadius: '50%', marginLeft: 'auto', marginRight: 'auto'}}>
                                                        <Container style={{paddingTop: '14px'}}>
                                                            <div style={{backgroundColor: '#FFFFFF', height: '120px', width: '120px', borderRadius: '50%', marginLeft: 'auto', marginRight: 'auto'}}>
                                                                <h5 style={{'paddingTop': '25px'}}>
                                                                    {maximum_possible_up_move} %
                                                                </h5>
                                                                <p style={{fontSize: '13px'}}>
                                                                    Maximum possible up move
                                                                </p>
                                                            </div>
                                                        </Container>
                                                    </div>
                                                </Container>
                                                <br/>
                                            </Col>
                                            <Col sm='6'>
                                                <Container>
                                                    <div style={{backgroundColor: 'red', height: '150px', width: '150px', borderRadius: '50%', marginLeft: 'auto', marginRight: 'auto'}}>
                                                        <Container style={{paddingTop: '14px'}}>
                                                            <div style={{backgroundColor: '#FFFFFF', height: '120px', width: '120px', borderRadius: '50%', marginLeft: 'auto', marginRight: 'auto'}}>
                                                                <h5 style={{'paddingTop': '25px'}}>
                                                                    {maximum_possible_down_move} %
                                                                </h5>
                                                                <p style={{fontSize: '13px'}}>
                                                                    Maximum possible down move
                                                                </p>
                                                            </div>
                                                        </Container>
                                                    </div>
                                                </Container>
                                                <br/>
                                            </Col>
                                        </Row>
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Row style={{margin: '0px', textAlign: 'left'}}>
                                            <Col sm='6' style={{fontWeight: 'bold', color: 'green'}}>
                                                Up-move risk-to-reward ratio:
                                                <br/>
                                            </Col>
                                            <Col>
                                                <span style={{fontWeight: 'bold'}}>1:{up_reward} </span>
                                                <span style={{fontSize: '13px'}}>(Risk: 1, Reward: : {up_reward})</span>
                                                <br/>
                                            </Col>
                                        </Row>
                                        <br/>
                                        <Row style={{margin: '0px', textAlign: 'left'}}>
                                            <Col sm='6' style={{fontWeight: 'bold', color: 'red'}}>
                                                Down-move risk-to-reward ratio:
                                                <br/>
                                            </Col>
                                            <Col>
                                                <span style={{fontWeight: 'bold'}}>1:{down_reward} </span>
                                                <span style={{fontSize: '13px'}}>(Risk: 1, Reward: {down_reward})</span>
                                                <br/>
                                            </Col>
                                        </Row>
                                    </Col>
                                </Row>
                                <br/><br/>
                                <h6 style={{fontWeight: 'bold', color: '#005fc9'}}>
                                    Price based analysis:
                                </h6>
                                <br/><br/>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='6' style={{fontWeight: 'bold'}}>
                                        Recent 15 minute close:
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Your broker's most recent 15 minute closing price" name="user_last_m15_close" id="user_last_m15_close"
                                            value={this.state.user_last_m15_close} onChange={this.HandleChange} type="number" 
                                        />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='6' style={{fontWeight: 'bold', color: 'green'}}>
                                        Up-move possible max price:
                                        <br/>
                                    </Col>
                                    <Col>
                                        <span style={{fontWeight: 'bold'}}>
                                            {
                                                this.state.user_last_m15_close === null || this.state.user_last_m15_close == 0 || this.state.user_last_m15_close === ''
                                                ? <>
                                                    Waiting for price input
                                                </>
                                                : <>
                                                    {up_move_possible_maximum_price}
                                                </>
                                            }    
                                        </span>
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='6' style={{fontWeight: 'bold', color: 'red'}}>
                                        Down-move possible max price:
                                        <br/>
                                    </Col>
                                    <Col>
                                        <span style={{fontWeight: 'bold'}}>
                                            {
                                                this.state.user_last_m15_close === null || this.state.user_last_m15_close == 0 || this.state.user_last_m15_close === ''
                                                ? <>
                                                    Waiting for price input
                                                </>
                                                : <>
                                                    {down_move_possible_maximum_price}
                                                </>
                                            }    
                                        </span>
                                        <br/>
                                    </Col>
                                </Row>
                            </div>
                        }
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Analysis);