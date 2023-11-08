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
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import { FaCalendarDay, FaCalendarWeek } from 'react-icons/fa';

class PaymentsList extends Component{
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
            end_of_list: true,
            on_mobile: false,
            start_date: '',
            end_date: '',
            entered_by: '', // firstname / lastname / username
            payments_list: [
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
                {
                    date: '14/10/2023 11:15am',
                    purpose: 'subscription',
                    payment_method: 'VISA',
                    discount_applied: 0,
                    amount: 10,
                    entered_by: 'Michael Panashe Mudimbu'
                },
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

        this.GetPaymentsList = (get_all) => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            var data = new FormData()
            data.append('start_date', this.state.start_date)
            data.append('end_date', this.state.end_date)
            data.append('entered_by', this.state.entered_by)
            data.append('length_of_data_received', this.state.payments_list.length)
            data.append('get_all', get_all) // bool

            axios.post(Backend_Server_Address + 'getPaymentsList', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set payments list to state
                this.setState({payments_list: result})
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
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, () => this.GetPaymentsList(get_all))
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, () => this.GetPaymentsList(get_all))
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, () => this.GetPaymentsList(get_all))
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, () => this.GetPaymentsList(get_all))
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
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Payments List | {Platform_Name}</title>
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
                            Payments List
                        </h5>
                        <br/><br/>
                        <Row style={{margin: '0px'}}>
                            <Col sm='3' style={{textAlign: 'left', marginRight: '20px'}}>
                                <Label style={{color: '#00539C'}}>Start Date</Label>
                                <InputGroup>
                                    <InputGroupText addonType="prepend">
                                        <FaCalendarDay style={{margin:'10px'}}/>
                                    </InputGroupText>
                                    <Input style={{border: 'none', color: 'inherit', backgroundColor: 'inherit'}}
                                        name="start_date" id="start_date"
                                        value={this.state.start_date} onChange={this.HandleChange} type="date" 
                                    />
                                </InputGroup>
                            </Col>
                            <Col sm='3' style={{textAlign: 'left', marginRight: '30px'}}>
                                <Label style={{color: '#00539C'}}>End Date</Label>
                                <InputGroup>
                                    <InputGroupText addonType="prepend">
                                        <FaCalendarWeek style={{margin:'10px'}}/>
                                    </InputGroupText>
                                    <Input style={{border: 'none', color: 'inherit', backgroundColor: 'inherit'}}
                                        name="end_date" id="end_date"
                                        value={this.state.end_date} onChange={this.HandleChange} type="date"  
                                    />
                                </InputGroup>
                            </Col>
                            <Col sm='4'>
                                <Col style={{textAlign: 'left', marginRight: '30px'}}>
                                    <Label style={{color: '#00539C'}}>Entered by</Label>
                                    <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                        placeholder="Staff's firstname / lastname / username" name="entered_by" id="entered_by"
                                        value={this.state.entered_by} onChange={this.HandleChange} type="text" 
                                    />
                                    <InputErrors field_error_state={this.state.input_errors['entered_by']} field_label='entered_by' />
                                </Col>
                            </Col>
                            <Col sm=''>
                                <br/>
                                <Button onClick={() => this.GetPaymentsList(false)} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    View
                                </Button>
                            </Col>
                        </Row>
                        <br/><br/>
                        <div style={{maxHeight: '450px', overflowY: 'scroll'}}>
                            <Table>
                                <thead>
                                    <tr style={{borderBottom: '1px solid silver'}}>
                                        <th width='20%'>Date</th>
                                        <th width='10%'>Purpose</th>
                                        <th width='10%'>Method</th>
                                        <th width='10%'>Discount</th>
                                        <th width='10%'>Amount</th>
                                        <th width='35%'>Entered by</th>
                                    </tr>
                                </thead>
                                <tbody style={{textAlign: 'left'}}>
                                    {
                                        this.state.payments_list.map((item, index) => {
                                            return <tr style={{borderBottom: '1px solid silver'}}>
                                                <td>{item.date}</td>
                                                <td>{item.purpose}</td>
                                                <td>{item.payment_method}</td>
                                                <td>% {item.discount_applied}</td>
                                                <td>$ {item.amount}</td>
                                                <td>{item.entered_by}</td>
                                            </tr>
                                        })
                                    }
                                </tbody>
                            </Table>
                            <br/>
                            {
                                this.state.end_of_list === true
                                ? <p style={{color: '#00539C', fontWeight: 'bold'}}>All data loaded</p>
                                : <></>
                            }
                            <br/>
                            <Button onClick={() => {this.GetPaymentsList(false); this.setState({end_of_list: false})}} 
                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                            >
                                Load more
                            </Button>
                            {' '}
                            <Button onClick={() => {this.GetEarningsReport(true); this.setState({end_of_list: false})}} 
                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                            >
                                Load all
                            </Button>
                            <br/><br/>
                        </div>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(PaymentsList);