import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Table, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupAddon,
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
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";

class PastPayments extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            past_payments: []
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // if field error state doesn't already exist
            if (this.state.input_errors[field] == undefined){
                // new error
                var new_error = {
                    [field]: error
                }

                // existing errors + new
                var updated_input_errors = {
                    ...this.state.input_errors,
                    ...new_error
                }

                // update state
                this.setState({input_errors: updated_input_errors})
            }else{ // field error state already exists
                // existing errors
                var existing_errors = this.state.input_errors

                // existing errors modified
                existing_errors[field] = error

                // update state
                this.setState({input_errors: existing_errors})
            }
        }

        this.ClearInputErrors = () => {
            this.setState({input_errors: {}})
        }

        this.Notification = (message, message_type) => { // message type -> info / success / warning / error
            const toaster = useToaster();
            
            // push notification message
            toaster.push(<Message>{message}</Message>, {
                placement: 'topCenter',
                closable: true,
                type: message_type,
                showIcon: true,
                duration: 15000
            });
        }

        this.GetUserPastPayments = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            axios.post(Backend_Server_Address + 'getUserPaymentHistory', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set past payments to state
                this.setState({past_payments: result, loading: false})
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
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }
    }

    componentDidMount() {
        this.GetUserPastPayments()
    }

    render() {
        var past_payments = this.state.past_payments
        var past_payments_map = past_payments.map((item, index) => {
            return<tr style={{borderBottom: '1px solid grey'}}>
                <td>{user.date}</td>
                <td>{user.purpose}</td>
                <td>{user.payment_method}</td>
                <td>{user.amount}</td>
            </tr>
        })

        return (
            <div>
                <Helmet>
                    <title>Past Payments | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            Past Payments
                        </h5>
                        <br/><br/>
                        <Table>
                            <thead>
                                <tr>
                                    <th width='25%'>Date</th>
                                    <th width='25%'>Purpose</th>
                                    <th width='25%'>Method</th>
                                    <th width='25%'>Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                {past_payments_map}
                            </tbody>
                        </Table>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(PastPayments);