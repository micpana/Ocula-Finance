import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Table, 
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

class PastPayments extends Component{
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
            past_payments: [
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    amount: 10
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'Mastercard',
                    amount: 96
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'Paypal',
                    amount: 10
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    amount: 10
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'Mastercard',
                    amount: 96
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'Paypal',
                    amount: 10
                }
            ]
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

        this.GetUserPastPayments = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getUserPaymentHistory', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set past payments to state
                this.setState({past_payments: result})
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
                        this.NetworkErrorScreenOn(notification_message, this.GetUserPastPayments)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetUserPastPayments)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetUserPastPayments)
                }
                this.LoadingOff()
            })
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // this.GetUserPastPayments()
    }

    render() {
        var past_payments = this.state.past_payments
        var past_payments_map = past_payments.map((item, index) => {
            return <tr style={{borderBottom: '1px solid silver'}}>
                <td>{item.date}</td>
                <td>{item.purpose}</td>
                <td>{item.payment_method}</td>
                <td>$ {item.amount}</td>
            </tr>
        })

        return (
            <div>
                <Helmet>
                    <title>Past Payments | {Platform_Name}</title>
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
                            Past Payments
                        </h5>
                        <br/><br/>
                        <div style={{maxHeight: '450px', overflowY: 'scroll'}}>
                            <Table>
                                <thead>
                                    <tr style={{borderBottom: '1px solid silver'}}>
                                        <th width='25%'>Date</th>
                                        <th width='25%'>Purpose</th>
                                        <th width='25%'>Method</th>
                                        <th width='25%'>Amount</th>
                                    </tr>
                                </thead>
                                <tbody style={{textAlign: 'left'}}>
                                    {past_payments_map}
                                </tbody>
                            </Table>
                        </div>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(PastPayments);