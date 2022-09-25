import Vue from 'vue'
import Router from 'vue-router'
// import Cookies from 'js-cookie'

Vue.use(Router);

function loadView(view) {
    return () => import(/* webpackChunkName: "view-[request]" */ `../components/${view}.vue`)
}

Vue.use(Router);

const router = new Router({
    // ordinary user pages
    routes: [{
        path: '/', component: loadView('TabbarFrame'), children: [{
            path: 'events', name: 'events', component: loadView('events/index')
        }, {
            path: 'positions', name: 'positions', component: loadView('HelloWorld')
        }, {
            path: '', name: 'dashboard', component: loadView('dashboard/index')
        }, {
            path: 'matching', name: 'matching', component: loadView('matching/index')
        }, {
            path: 'paper_list/:type', name: 'paper_list', component: loadView('dashboard/papers')
        }, {
            path: 'ans_paper/:id', name: 'ans_paper', component: loadView('dashboard/answer_paper')
        }, {
            path: 'view_paper/:id', name: 'view_paper', component: loadView('dashboard/review_paper')
        }, {
            path: 'events/list/:type', name: 'events_list', component: loadView('events/events_list')
        }, {
            path: 'events/view/:id', name: 'events_details', component: loadView('events/events_details')
        }]
    }, {path: '/login', name: 'login', component: loadView('account/index')}, {path: 'register'}]
});


export default router
