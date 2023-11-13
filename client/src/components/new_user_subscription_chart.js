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
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FaCalendarDay, FaCalendarWeek } from 'react-icons/fa';

class NewUserSubscriptionChart extends Component{
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
            start_date: '',
            end_date: '',
            category: 'Daily', // Daily / Monthly / Yearly
            categories: ['Daily', 'Monthly', 'Yearly'],
            new_user_subscription_statistics: []
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

        this.GetNewUserSubscriptionStatistics = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            var data = new FormData()
            data.append('start_date', this.state.start_date)
            data.append('end_date', this.state.end_date)
            data.append('category', this.state.category)

            axios.post(Backend_Server_Address + 'getNewSubscribedUserCountStatistics', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set new user subscription statistics to state
                this.setState({new_user_subscription_statistics: result})
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
                        this.NetworkErrorScreenOn(notification_message, this.GetNewUserSubscriptionStatistics)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetNewUserSubscriptionStatistics)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetNewUserSubscriptionStatistics)
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
        this.GetNewUserSubscriptionStatistics()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>New User Subscription Chart | {Platform_Name}</title>
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
                            New User Subscription Chart
                        </h5>
                        <br/><br/>
                        <Row style={{margin: '0px'}}>
                            <Col sm='3' style={{textAlign: 'left', marginRight: '20px'}}>
                                <Label style={{fontWeight: 'bold'}}>Category:</Label>
                                <select name='category' value={this.state.category} onChange={this.HandleChange}
                                    style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                >
                                    {
                                        this.state.categories.map((item) => {
                                            return<option value={item}>{item}</option>
                                        })
                                    }
                                </select>
                            </Col>
                        </Row>
                        <br/>
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
                            <Col sm='3'>
                                <br/>
                                <Button onClick={this.GetNewUserSubscriptionStatistics} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    View
                                </Button>
                            </Col>
                        </Row>
                        <br/><br/><br/>
                        <div style={{width: '100%', overflowX: 'scroll'}}>
                            <BarChart
                                width={1000}
                                height={300}
                                data={this.state.new_user_subscription_statistics}
                                margin={{
                                    top: 0, right: 0, left: 0, bottom: 0,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="users" fill="#F2B027" />
                            </BarChart>
                        </div>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(NewUserSubscriptionChart);