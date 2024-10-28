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
import DateTimeDisplay from './timezone_conversion'
import Ecocash from '../images/ecocash.png'
import OneMoney from '../images/one_money.jpeg'
import Bitcoin from '../images/bitcoin.svg'
import Ethereum from '../images/ethereum.svg'
import USDCoin from '../images/usd-coin.svg'
import Tron from '../images/tron.svg'
import Tether from '../images/tether.svg'
import BNB from '../images/bnb.svg'
import Dogecoin from '../images/dogecoin.svg'
import Litecoin from '../images/litecoin.svg'
import Digibyte from '../images/digibyte.svg'
import Monero from '../images/monero.svg'
import Ton from '../images/ton.svg'
import Polygon from '../images/polygon.svg'
import BitcoinCash from '../images/bitcoin-cash.svg'
import ShibaInu from '../images/shiba-inu.svg'
import Solana from '../images/solana.svg'
import Notcoin from '../images/notcoin.svg'
import Dogs from '../images/dogs.svg'
import { FaMoneyBill, FaPhone } from 'react-icons/fa';

class Subscriptions extends Component{
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
            user_details: {},
            method: 'EcoCash', // EcoCash / OneMoney
            methods: ['EcoCash', 'OneMoney'],
            phonenumber: '',
            currency: 'USD', // USD / ZWG
            currencies: ['USD', 'ZWG'],
            subscription_type: 'Monthly Subscription', // Monthly Subscription / Yearly Subscription
            subscription_types: ['Monthly Subscription', 'Yearly Subscription']
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

        this.GetUserDetails = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getUserDetailsByAccessToken', null, { headers: { 'Access-Token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set user details to state
                this.setState({user_details: result})
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
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, this.GetUserDetails)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetUserDetails)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetUserDetails)
                }
                this.LoadingOff()
            })
        }

        this.InitializeOxapayPayment = () => {

        }

        this.VerifyOxapayPayment = () => {

        }

        this.InitializePaynowPayment = () => {

        }

        this.VerifyPaynowPayment = () => {

        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        this.GetUserDetails()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Subscriptions | {Platform_Name}</title>
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
                            Subscriptions
                        </h5>
                        <br/><br/>
                        <Row style={{margin: '0px', textAlign: 'left', fontSize: '13px'}}>
                            <Col sm='6'>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <span style={{fontWeight: 'bold'}}>
                                            Your current subscription status:
                                        </span>
                                    </Col>
                                    <Col>
                                        {
                                            this.state.user_details.subscribed === true
                                            ? <div style={{fontWeight: 'bold', color: 'green'}}>
                                                Subscribed
                                            </div> 
                                            : <div style={{fontWeight: 'bold', color: 'red'}}>
                                                Not subscribed
                                            </div>
                                        }
                                    </Col>
                                </Row>
                                <br/>
                            </Col>
                            <Col>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <span style={{fontWeight: 'bold'}}>
                                            Subscription expiry date:
                                        </span>
                                    </Col>
                                    <Col>
                                        <div style={{fontWeight: 'bold', color: '#00539C'}}>
                                            {
                                                this.state.user_details.subscription_expiry === ''
                                                ? <>
                                                    You've never subscribed before
                                                </>
                                                : <>
                                                    <DateTimeDisplay datetimeString={this.state.user_details.subscription_expiry} />
                                                </>
                                            }
                                        </div>
                                    </Col>
                                </Row>
                                <br/>
                            </Col>
                        </Row>
                        <Row style={{margin: '0px'}}>
                            <Col sm='3' style={{textAlign: 'left'}}>
                                <Label style={{fontWeight: 'bold'}}>Subscription Package:</Label>
                                <select name='subscription_type' value={this.state.subscription_type} onChange={this.HandleChange}
                                    style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                >
                                    {
                                        this.state.subscription_types.map((item) => {
                                            return<option value={item}>{item}</option>
                                        })
                                    }
                                </select>
                            </Col>
                        </Row>
                        <Row style={{margin: '0px', marginTop: '15px'}}>
                            <Col sm='6'>
                                <Container>
                                    <span style={{fontWeight: 'bold'}}>
                                        Pay using Crypto
                                    </span>
                                    <br/><br/>
                                    <p style={{textAlign: 'left'}}>
                                        We accept <img src={Bitcoin} style={{width: '20px'}}/>Bitcoin,
                                        {' '}<img src={Ethereum} style={{width: '20px'}}/>Ethereum, <img src={USDCoin} style={{width: '20px'}}/>USD Coin,
                                        {' '}<img src={Tron} style={{width: '20px'}}/>Tron, <img src={Tether} style={{width: '20px'}}/>Tether,
                                        {' '}<img src={BNB} style={{width: '20px'}}/>BNB, <img src={Dogecoin} style={{width: '20px'}}/>Dogecoin,
                                        {' '}<img src={Litecoin} style={{width: '20px'}}/>Litecoin, <img src={Digibyte} style={{width: '20px'}}/>Digibyte,
                                        {' '}<img src={Monero} style={{width: '20px'}}/>Monero, <img src={Ton} style={{width: '20px'}}/>Ton,
                                        {' '}<img src={Polygon} style={{width: '20px'}}/>Polygon, <img src={BitcoinCash} style={{width: '20px'}}/>Bitcoin Cash,
                                        {' '}<img src={ShibaInu} style={{width: '20px'}}/>Shiba Inu, <img src={Solana} style={{width: '20px'}}/>Solana,
                                        {' '}<img src={Notcoin} style={{width: '20px'}}/>Notcoin, <img src={Dogs} style={{width: '20px'}}/>Dogs
                                    </p>
                                    <p style={{textAlign: 'left', fontSize: '13px'}}>
                                        Click on 'Pay' to make a payment, you'll be taken to a Oxapay page to make a payment using your preferred 
                                        currency. After you've successfully made a payment, you can come back here and click on 'Verify payment'.
                                    </p>
                                    <br/>
                                    <Row style={{margin: '0px'}}>
                                        <Col sm='6'>
                                            <Button onClick={() => this.InitializeOxapayPayment()}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Pay
                                            </Button>
                                        </Col>
                                        <Col>
                                            <Button onClick={() => this.VerifyOxapayPayment()}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Verify payment
                                            </Button>
                                        </Col>
                                    </Row>
                                </Container>
                                <br/><br/>
                            </Col>
                            <Col>
                                <Container>
                                    <span style={{fontWeight: 'bold'}}>
                                        Pay using <span style={{color: '#0052A4'}}>Eco</span><span style={{color: '#E90000'}}>Cash</span> and {' '}
                                        <span style={{color: '#F6BE72'}}>One</span><span style={{color: '#061008'}}>Money</span>
                                    </span>
                                    <br/><br/>
                                    <p style={{textAlign: 'left'}}>
                                        We accept both USD and ZWG on <img src={Ecocash} style={{width: '20px'}}/>EcoCash, and only ZWG on
                                        {' '}<img src={OneMoney} style={{width: '20px'}}/>OneMoney
                                    </p>
                                    <Row style={{margin: '0px'}}>
                                        <Col sm='6' style={{textAlign: 'left'}}>
                                            <Label style={{fontWeight: 'bold'}}>Method:</Label>
                                            <select name='method' value={this.state.method} onChange={this.HandleChange}
                                                style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                            >
                                                {
                                                    this.state.methods.map((item) => {
                                                        return<option value={item}>
                                                            {
                                                                item == 'EcoCash'
                                                                ? <><span style={{color: '#0052A4'}}>Eco</span><span style={{color: '#E90000'}}>Cash</span></>
                                                                : <><span style={{color: '#F6BE72'}}>One</span><span style={{color: '#061008'}}>Money</span></>
                                                            }
                                                        </option>
                                                    })
                                                }
                                            </select>
                                        </Col>
                                        <Col style={{textAlign: 'left'}}>
                                            <Label style={{fontWeight: 'bold'}}>Currency:</Label>
                                            <select name='currency' value={this.state.currency} onChange={this.HandleChange}
                                                style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                            >
                                                {
                                                    this.state.currencies.map((item) => {
                                                        return<option value={item}>{item}</option>
                                                    })
                                                }
                                            </select>
                                        </Col>
                                    </Row>
                                    <br/>
                                    <Label style={{fontWeight: 'bold', textAlign: 'left'}}>Phonenumber <span style={{color: 'red'}}>*</span></Label>
                                    <InputGroup>
                                        <InputGroupText addonType="prepend">
                                            <FaMoneyBill style={{margin:'10px'}}/>
                                        </InputGroupText>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="eg 0777000111 / 0717000111" name="phonenumber" id="phonenumber"
                                            value={this.state.phonenumber} onChange={this.HandleChange} type="text" 
                                        />
                                    </InputGroup>
                                    <InputErrors field_error_state={this.state.input_errors['phonenumber']} field_label='Phonenumber' />
                                    <br/>
                                    <p style={{textAlign: 'left', fontSize: '13px'}}>
                                        Click on 'Pay' to make a payment, you'll be prompted to enter your EcoCash or OneMoney pin on your 
                                        mobile device to confirm the payment. After you've successfully made a payment, you can come back here 
                                        and click on 'Verify payment'.
                                    </p>
                                    <br/>
                                    <Row style={{margin: '0px'}}>
                                        <Col sm='6'>
                                            <Button onClick={() => this.InitializePaynowPayment()}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Pay
                                            </Button>
                                        </Col>
                                        <Col>
                                            <Button onClick={() => this.VerifyPaynowPayment()}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Verify payment
                                            </Button>
                                        </Col>
                                    </Row>
                                </Container>
                            </Col>
                        </Row>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Subscriptions);