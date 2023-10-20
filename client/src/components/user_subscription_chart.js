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
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, Cell} from 'recharts';

class UserSubscriptionChart extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            on_mobile: false,
            user_subscription_statistics: [
                {
                    date: '14/11/2023',
                    users: 30
                },
                {
                    date: '15/11/2023',
                    users: 300
                },
                {
                    date: '16/11/2023',
                    users: 120
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

        this.GetUserSubscriptionStatistics = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            axios.post(Backend_Server_Address + 'getSubscribedUserCountStatistics', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set users to state
                this.setState({user_subscription_statistics: result, loading: false})
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'Access token disabled via signout' ||
                        result === 'Access token expired' ||
                        result === 'Not authorized to access this' ||
                        result === 'Invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // this.GetUserSubscriptionStatistics()
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>User Subscription Chart | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            User Subscription Chart
                        </h5>
                        <br/><br/><br/><br/>
                        <div style={{width: '100%', overflowX: 'scroll'}}>
                            <LineChart
                                width={1000}
                                height={300}
                                data={this.state.user_subscription_statistics}
                                margin={{
                                    top: 0, right: 0, left: 0, bottom: 0,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="users" stroke="#00539C" activeDot={{ r: 8 }}/>
                            </LineChart>
                        </div>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(UserSubscriptionChart);