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
import { User_Roles, Payment_Purposes, Payment_Methods} from './lists'
import { FaEdit, FaKey, FaMoneyBill, FaMoneyCheckAlt, FaNotesMedical, FaSearch } from 'react-icons/fa';

class AllUsers extends Component{
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
            screen: 'users', // users / user / selected user payments
            to_show_list: ['All', 'Subscribed', 'Not subscribed', 'Banned', 'Verified', 'Not verified'],
            users_showing: 'All', // All / Subscribed / Not subscribed / Banned / Verified / Not verified
            all_users: [
                {
                    _id: {'$oid': 'shgugudyufhbdfu'},
                    firstname: 'Michael',
                    lastname: 'Mudimbu',
                    username: 'micpana',
                    email: 'michaelmudimbu@gmail.com',
                    phonenumber: '+263782464219',
                    country: 'Zimbabwe',
                    date_of_registration: '14/10/2023 11:15am',
                    verified: true,
                    subscribed: true,
                    subscription_date: '14/10/2023 11:15am',
                    subscription_expiry: '14/11/2023 11:15am',
                    role: 'admin',
                    banned: false
                }
            ],
            user: null,
            user_payments: [
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
            ],
            search_query: '',
            user_metrics: {
                all_users: 10000,
                subscribed_users: 9700,
                users_not_subscribed: 300,
                banned_users: 20,
                verified_users: 9900,
                users_not_verified: 100
            },
            password: '',
            ban_reason: '',
            new_role: '',
            purpose: '',
            payment_method: '',
            transaction_id: '',
            verified: false,
            discount_applied: 0,
            amount: 0
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

        this.GetAllUsers = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getAllUsers', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set users to state
                this.setState({all_users: result})
                this.LoadingOff()
                this.GetUserMetrics()
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
                        this.NetworkErrorScreenOn(notification_message, this.GetAllUsers)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetAllUsers)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetAllUsers)
                }
                this.LoadingOff()
            })
        }

        this.GetSelectedUserPayments = (user_id) => {
            const { cookies } = this.props;
            this.LoadingOn()
            
            var data = new FormData()
            data.append('account_id', user_id)

            axios.post(Backend_Server_Address + 'getUserPaymentHistoryByAccountId', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set user payments to state and switch to user payments screen
                this.setState({user_payments: result, screen: 'selected user payments'})
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
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                }
                this.LoadingOff()
            })
        }

        this.SearchForUser = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.search_query === ''){ this.SetInputError('search_query', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.LoadingOn()

                var data = new FormData()
                data.append('search_query', this.state.search_query)

                axios.post(Backend_Server_Address + 'searchForUser', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // set user results to state
                    this.setState({all_users: result})
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
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        } 

        this.GetUserMetrics = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getUserMetrics', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set users to state
                this.setState({user_metrics: result})
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
                        this.NetworkErrorScreenOn(notification_message, this.GetAllUsers)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.GetAllUsers)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.GetAllUsers)
                }
                this.LoadingOff()
            })
        }

        this.BanUser = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.ban_reason === ''){ this.SetInputError('ban_reason', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.LoadingOn()

                var data = new FormData()
                data.append('account_id', this.state.user._id.$oid)
                data.append('ban_reason', this.state.ban_reason)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'banUser', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // clear password and ban reason in state
                    this.setState({
                        ban_reason: '',
                        password: ''
                    })
                    // update user details in state
                    var all_users = this.state.all_users
                    all_users.map((item, index) => {
                        if (item._id.$oid === this.state.user._id.$oid){
                            // update user details
                            var user = item
                            user['banned'] = true
                            // modify user details in main list
                            all_users[index] = user
                            // set modified list to state
                            this.setState({
                                all_users: all_users
                            })
                        }
                    })
                    // success notification + loading off
                    Notification('User ban successful.', 'success')
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
                        }else if(result === 'incorrect password'){
                            Notification("You've entered an incorrect password.", 'error')
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        }

        this.UnbanUser = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.LoadingOn()

                var data = new FormData()
                data.append('account_id', this.state.user._id.$oid)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'unbanUser', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // clear password in state
                    this.setState({
                        password: ''
                    })
                    // update user details in state
                    var all_users = this.state.all_users
                    all_users.map((item, index) => {
                        if (item._id.$oid === this.state.user._id.$oid){
                            // update user details
                            var user = item
                            user['banned'] = false
                            // modify user details in main list
                            all_users[index] = user
                            // set modified list to state
                            this.setState({
                                all_users: all_users
                            })
                        }
                    })
                    // success notification + loading off
                    Notification('User unban successful.', 'success')
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
                        }else if(result === 'incorrect password'){
                            Notification("You've entered an incorrect password.", 'error')
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        }

        this.ChangeUserRole = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.new_role === ''){ this.SetInputError('new_role', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.LoadingOn()

                var data = new FormData()
                data.append('account_id', this.state.user._id.$oid)
                data.append('new_role', this.state.new_role)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'changeUserRole', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // clear password and new_role in state
                    this.setState({
                        new_role: '',
                        password: ''
                    })
                    // update user details in state
                    var all_users = this.state.all_users
                    all_users.map((item, index) => {
                        if (item._id.$oid === this.state.user._id.$oid){
                            // update user details
                            var user = item
                            user['role'] = this.state.new_role
                            // modify user details in main list
                            all_users[index] = user
                            // set modified list to state
                            this.setState({
                                all_users: all_users
                            })
                        }
                    })
                    // success notification + loading off
                    Notification('User role change successful.', 'success')
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
                        }else if(result === 'incorrect password'){
                            Notification("You've entered an incorrect password.", 'error')
                        }else if(result === 'invalid role'){
                            Notification("You've entered an invalid user role.", 'error')
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        }

        this.ManuallyEnterUserPayment = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.purpose === ''){ this.SetInputError('purpose', 'required'); data_checks_out = false }
            if (this.state.payment_method === ''){ this.SetInputError('payment_method', 'required'); data_checks_out = false }
            if (this.state.transaction_id === ''){ this.SetInputError('transaction_id', 'required'); data_checks_out = false }
            if (this.state.verified === ''){ this.SetInputError('verified', 'required'); data_checks_out = false }
            if (this.state.discount_applied === null){ this.SetInputError('discount_applied', 'required'); data_checks_out = false }
            if (this.state.discount_applied < 0 || this.state.discount_applied > 100){ this.SetInputError('discount_applied', 'invalid'); data_checks_out = false }
            if (this.state.amount === 0 || this.state.amount === null){ this.SetInputError('amount', 'required'); data_checks_out = false }
            if (this.state.amount < 0){ this.SetInputError('amount', 'invalid'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                const { cookies } = this.props;
                this.LoadingOn()

                var data = new FormData()
                data.append('account_id', this.state.user._id.$oid)
                data.append('purpose', this.state.purpose)
                data.append('payment_method', this.state.payment_method)
                data.append('transaction_id', this.state.transaction_id)
                data.append('verified', this.state.verified)
                data.append('discount_applied', this.state.discount_applied)
                data.append('amount', this.state.amount)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'manuallyEnterUserPayment', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
                .then((res) => {
                    let result = res.data
                    // clear request related data in state... alse set screen to 'user', so that payments have to be reloaded to view them again
                    this.setState({
                        purpose: '',
                        payment_method: '',
                        transaction_id: '',
                        verified: false,
                        discount_applied: 0,
                        amount: 0,
                        password: '',
                        screen: 'user'
                    })
                    // success notification + loading off
                    Notification('Payment addition successful.', 'success')
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
                        }else if(result === 'enter sufficient amount for a subscription'){
                            Notification("Enter a sufficient amount for a subscription.", 'error')
                        }else if(result === 'subscription amount cannot be more than max subscription'){
                            Notification("The subscription amount cannot be more than the max subscription amount.", 'error')
                        }else if(result === 'incorrect password'){
                            Notification("You've entered an incorrect password.", 'error')
                        }else if(result === 'invalid purpose'){
                            Notification("You've entered an invalid payment purpose.", 'error')
                        }else if(result === 'invalid method'){
                            Notification("You've entered an invalid payment method.", 'error')
                        }else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
        }
    }
    
    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // this.GetAllUsers()
    }

    render() {
        // active screen
        var screen = this.state.screen
        // users
        var to_show = this.state.users_showing
        var all_users = this.state.all_users
        
        var users_to_show = []
        if (to_show === 'All'){ users_to_show = all_users }
        if (to_show === 'Subscribed'){ users_to_show = all_users.filter(item => item.subscribed === true) }
        if (to_show === 'Not subscribed'){ users_to_show = all_users.filter(item => item.subscribed === false) }
        if (to_show === 'Banned'){ users_to_show = all_users.filter(item => item.banned === true) }
        if (to_show === 'Verified'){ users_to_show = all_users.filter(item => item.verified === true) }
        if (to_show === 'Not verified'){ users_to_show = all_users.filter(item => item.verified === false) }

        var users_to_show_map = users_to_show.map((item, index) => {
            return <tr onClick={() => {this.setState({user: item, screen: 'user'}); window.scrollTo(0, 0)}}
                style={{borderBottom: '1px solid silver', cursor: 'pointer'}}
            >
                <td>{item.firstname}</td>
                <td>{item.lastname}</td>
                <td>{item.username}</td>
                <td>{item.email}</td>
            </tr>
        })
        // user
        var user = this.state.user
        var user_payments = this.state.user_payments
        var user_payments_map = user_payments.map((item, index) => {
            return <tr style={{borderBottom: '1px solid silver'}}>
                <td>{item.date}</td>
                <td>{item.purpose}</td>
                <td>{item.payment_method}</td>
                <td>$ {item.amount}</td>
            </tr>
        })
        // users metrics
        var user_metrics = this.state.user_metrics

        return (
            <div>
                <Helmet>
                    <title>All Users | {Platform_Name}</title>
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
                            All Users
                        </h5>
                        <br/><br/>
                        {
                            screen === 'users'
                            ? <>
                                <h6 style={{color: '#00539C', textAlign: 'left'}}>User metrics:</h6>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>All:</span> {user_metrics.all_users}
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>Subscribed:</span> {user_metrics.subscribed_users}
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>Not subscribed:</span> {user_metrics.users_not_subscribed}
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>Banned:</span> {user_metrics.banned_users}
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>Verified:</span> {user_metrics.verified_users}
                                    </Col>
                                    <Col sm=''>
                                        <span style={{fontWeight: 'bold'}}>Not verified:</span> {user_metrics.users_not_verified}
                                    </Col>
                                </Row>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='3' style={{textAlign: 'left', marginRight: '20px'}}>
                                        <Label style={{fontWeight: 'bold'}}>Users to view:</Label>
                                        <select name='users_showing' value={this.state.users_showing} onChange={this.HandleChange}
                                            style={{border: 'none', borderBottom: '1px solid #F2B027', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                        >
                                            {
                                                this.state.to_show_list.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                    </Col>
                                    <Col style={{textAlign: 'left', marginRight: '30px'}}>
                                        <Label style={{color: '#00539C'}}>Search for user</Label>
                                        <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                            placeholder="Search using user's email / username / names / phonenumber" name="search_query" id="search_query"
                                            value={this.state.search_query} onChange={this.HandleChange} type="text" 
                                        />
                                        <InputErrors field_error_state={this.state.input_errors['search_query']} field_label='Search Query' />
                                    </Col>
                                    <Col sm='3'>
                                        <br/>
                                        <Button onClick={this.SearchForUser} 
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                        >
                                            Search <FaSearch style={{marginLeft: '20px'}}/>
                                        </Button>
                                    </Col>
                                </Row>
                                <br/><br/><br/>
                                <div style={{maxHeight: '450px', overflowY: 'scroll'}}>
                                    <Table>
                                        <thead>
                                            <tr style={{borderBottom: '1px solid silver'}}>
                                                <th width='25%'>Firstname</th>
                                                <th width='25%'>Lastname</th>
                                                <th width='25%'>Username</th>
                                                <th width='25%'>Email</th>
                                            </tr>
                                        </thead>
                                        <tbody style={{textAlign: 'left'}}>
                                            {users_to_show_map}
                                        </tbody>
                                    </Table>
                                </div>
                            </>
                            : screen === 'user'
                            ? <>
                                <div style={{textAlign: 'left'}}>
                                    <Button onClick={() => {this.setState({screen: 'users', user: null}); window.scrollTo(0, 0)}}
                                        style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                    >
                                        {'<<<'} Back
                                    </Button>
                                </div>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <div style={{border: '1px solid grey', borderRadius: '20px', minHeight: '100px', maxHeight: '700px', overflow: 'scroll'}}>
                                            <br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>
                                                User Information
                                            </h6>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Firstname:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.firstname}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Lastname:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.lastname}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Username:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.username}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Email:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.email}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Phonenumber:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.phonenumber}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Country:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.country}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Date of registration:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.date_of_registration}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Verified:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.verified === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscribed:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.subscribed === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscription Date:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.subscription_date}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscription Expiry:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.subscription_expiry}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Account type:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.role}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Role issued by:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.role_issued_by}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Banned:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.banned === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Banned by:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.banned_by}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Ban reason:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.ban_reason}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Unbanned by:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.unbanned_by}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Ban time:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.ban_time}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Unban time:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.unban_time}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/><br/><br/>
                                        </div>
                                    </Col>
                                    <Col>
                                        <div style={{border: '1px solid grey', borderRadius: '20px', maxHeight: '700px', overflow: 'scroll'}}>
                                            <br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>User Payments</h6>
                                            <br/>
                                            <Button onClick={() => {this.GetSelectedUserPayments(user._id.$oid); window.scrollTo(0, 0)}}
                                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                <FaMoneyCheckAlt /> View user payments
                                            </Button>
                                            <br/><br/><br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>Ban User</h6>
                                            <br/>
                                            <Label>Ban Reason <span style={{color: 'red'}}>*</span></Label>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Ban reason" name="ban_reason" id="ban_reason"
                                                value={this.state.ban_reason} onChange={this.HandleChange} type="textarea" rows={3} 
                                            />
                                            <InputErrors field_error_state={this.state.input_errors['ban_reason']} field_label='Ban Reason' />
                                            <br/>
                                            <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password" 
                                            />
                                            <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                            <br/>
                                            <Button onClick={this.BanUser}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Ban user
                                            </Button>
                                            <br/><br/><br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>Unban User</h6>
                                            <br/>
                                            <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password" 
                                            />
                                            <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                            <br/>
                                            <Button onClick={this.UnbanUser}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Unban user
                                            </Button>
                                            <br/><br/><br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>Change User Role</h6>
                                            <br/>
                                            <Label>New role: <span style={{color: 'red'}}>*</span></Label>
                                            <select name='symbol' value={this.state.new_role} onChange={this.HandleChange}
                                                style={{marginTop: '28px', border: 'none', borderBottom: '1px solid #828884', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                            >
                                                <option value=''>Select new user role</option>
                                                {
                                                    User_Roles.map((item) => {
                                                        return<option value={item}>{item}</option>
                                                    })
                                                }
                                            </select>
                                            <InputErrors field_error_state={this.state.input_errors['new_role']} field_label='New Role' />
                                            <br/>
                                            <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password" 
                                            />
                                            <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                            <br/>
                                            <Button onClick={this.ChangeUserRole}
                                                style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                            >
                                                Change user role
                                            </Button>
                                            <br/><br/><br/>
                                        </div>
                                    </Col>
                                </Row>
                            </>
                            : screen === 'selected user payments'
                            ? <>
                                <div style={{textAlign: 'left'}}>
                                    <Button onClick={() => {this.setState({screen: 'user'}); window.scrollTo(0, 0)}}
                                        style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                    >
                                        {'<<<'} Back
                                    </Button>
                                </div>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col>
                                        <div style={{border: '1px solid grey', borderRadius: '20px', minHeight: '100px', maxHeight: '450px', overflowY: 'scroll'}}>
                                            <br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>
                                                {user.firstname} {user.lastname}'s Payments
                                            </h6>
                                            <br/>
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
                                                    {user_payments_map}
                                                </tbody>
                                            </Table>
                                            <br/>
                                        </div>
                                    </Col>
                                </Row>
                                <br/><br/><br/>
                                <h6 style={{fontWeight: 'bold', color: '#00539C'}}>
                                    Manually Enter Payment For: {user.firstname} {user.lastname}
                                </h6>
                                <br/><br/>
                                <Row>
                                    <Col sm='6'>
                                        <Label>Purpose <span style={{color: 'red'}}>*</span></Label>
                                        <select name='purpose' value={this.state.purpose} onChange={this.HandleChange}
                                            style={{marginTop: '28px', border: 'none', borderBottom: '1px solid #828884', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                        >
                                            <option value=''>Select purpose</option>
                                            {
                                                Payment_Purposes.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                        <InputErrors field_error_state={this.state.input_errors['purpose']} field_label='Purpose' />
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Label>Payment Method <span style={{color: 'red'}}>*</span></Label>
                                        <select name='payment_method' value={this.state.payment_method} onChange={this.HandleChange}
                                            style={{marginTop: '28px', border: 'none', borderBottom: '1px solid #828884', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                        >
                                            <option value=''>Select payment method</option>
                                            {
                                                Payment_Methods.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                        <InputErrors field_error_state={this.state.input_errors['payment_method']} field_label='Payment Method' />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row>
                                    <Col sm='6'>
                                        <Label>Transaction ID <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaEdit style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Transaction ID" name="transaction_id" id="transaction_id"
                                                value={this.state.transaction_id} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['transaction_id']} field_label='Transaction ID' />
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Label>Verified <span style={{color: 'red'}}>*</span></Label>
                                        <select name='verified' value={this.state.verified} onChange={this.HandleChange}
                                            style={{marginTop: '28px', border: 'none', borderBottom: '1px solid #828884', width: '100%', backgroundColor: 'inherit', color: '#00539C', outline: 'none'}}
                                        >
                                            <option value={false}>False</option>
                                            <option value={true}>True</option>
                                        </select>
                                        <InputErrors field_error_state={this.state.input_errors['verified']} field_label='Verified' />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row>
                                    <Col sm='6'>
                                        <Label>Discount Applied <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaMoneyCheckAlt style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="% Discount applied" name="discount_applied" id="discount_applied"
                                                value={this.state.discount_applied} onChange={this.HandleChange} type="number" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['discount_applied']} field_label='Discount Applied' />
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Label>Amount <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaMoneyBill style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Amount" name="amount" id="amount"
                                                value={this.state.amount} onChange={this.HandleChange} type="number" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['amount']} field_label='Amount' />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row>
                                    <Col sm='6'>
                                        <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaKey style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password"
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                        <br/>
                                    </Col>
                                    <Col>
                                            
                                    </Col>
                                </Row>
                                <br/><br/><br/>
                                <Button onClick={this.ManuallyEnterUserPayment}
                                    style={{width: '180px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Add User Payment
                                </Button>
                                <br/><br/><br/>
                            </>
                            : <>
                                <br/><br/><br/>
                                <h5 style={{color: '#005fc9'}}>Something went wrong.</h5>
                                <br/><br/><br/>
                                <Grid width='180px' style={{color: '#005fc9'}}/>
                            </>
                        }
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(AllUsers);