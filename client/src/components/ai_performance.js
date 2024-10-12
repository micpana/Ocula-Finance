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
import Deriv from '../images/deriv.png'
import { Model_Cards } from './model_cards'
import ModelCardRender from './model_card_render'

class AIPerformance extends Component{
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
            on_mobile: false
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
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

            if (base === '' && quote === ''){ // for synthetic indices
                return <Row style={{margin: '0px'}}>
                    <Col xs='6'>
                        
                    </Col>
                    <Col xs='6'>
                        <img src={Deriv} style={{width: '30px', height: '30px'}} />
                    </Col>
                </Row>
            }else{ // for forex and crypto pairs
                return <Row style={{margin: '0px'}}>
                    <Col xs='6'>
                        <img src={base} style={{width: '30px', height: '30px'}} />
                    </Col>
                    <Col xs='6'>
                        <img src={quote} style={{width: '30px', height: '30px'}} />
                    </Col>
                </Row>
            }
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
    }

    render() {
        var symbol_model_performances = Symbols.map((item, index) => {
            return <Col sm='6'>
                <div
                    style={{marginBottom: '30px', border: '1px solid #F2B027', borderRadius: '20px'}}
                >
                    <br/>
                    <Container>
                        <ModelCardRender symbol={item} />
                    </Container>
                </div>
            </Col>
        })

        return (
            <div>
                <Helmet>
                    <title>AI Performance | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <div style={{backgroundColor: '#005fc9', color: '#ffffff', minHeight: '200px', borderBottom: '1px solid #F9C961'}}>
                            <br/><br/><br/>
                            <h3 style={{fontWeight: 'bold'}}>
                                AI Performance
                            </h3>
                        </div>
                        <Container>
                            <br/><br/>
                            <p style={{textAlign: 'justify'}}>
                                Each instrument our AI analyses has its own seperate AI model, and each model has its own win rate. All our 
                                AI models have win rates that range above 80%, sticking to a minimum risk-to-reward ratio of 1:2. The performance 
                                metrics for each of our AI models are listed below.
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                {symbol_model_performances}
                            </Row>
                            <br/><br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#005fc9'}}>
                                Explore {Platform_Name} today and redefine your trading experience. 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                Join {Platform_Name} today and optimize your Forex Trading with the ultimate support of AI-powered 
                                analysis. We believe that technology and analytics should be affordable, simple, and impactful, 
                                offering each of our users more control over their trades.
                            </p>
                            <Row style={{margin: '0px'}}>
                                <Col sm='4'></Col>
                                <Col sm='4'></Col>
                                <Col sm='4'>
                                    <Button href='/signup' style={{backgroundColor: '#005fc9', color: '#ffffff', fontWeight: 'bold', border: '1px solid #005fc9', width: '180px'}}>
                                        Sign up
                                    </Button>
                                </Col>
                            </Row>
                        </Container>
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(AIPerformance);