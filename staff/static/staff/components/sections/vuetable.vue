<template>
    <div>
        <div class="ui form">
            <div class="fields">
                <div class="twelve wide field">
                    <div class="ui left icon fluid input">
                        <i class="search icon"></i>
                        <input type="text" class="searchText" placeholder="Search..." v-model="searchText">
                    </div>
                </div>
                <div class="four wide field">
                    <div id="user_drop" class="ui floating dropdown labeled icon button">
                        <i class="filter icon"></i>
                        <span class="text">Filter Posts</span>
                        <div class="menu">
                            <div class="header">
                                <i class="tags icon"></i>
                                Tag Label
                            </div>
                            <div class="scrolling menu">
                                <div v-for="option in options">
                                    <div data-value="option.text" class="item">
                                        <div v-bind:class="option.color" class="ui empty circular label"></div>
                                        option.text
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <table class="ui striped table userTable">
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Skills</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>

    </div>

</template>

<script>
    export default {
        data() {
            return {
                options: [
                    {text: 'Todos', color: 'red'},
                    {text: 'Hacker', color: 'blue'},
                    {text: 'Mentores', color: 'yellow'}
                ]
            }
        },
        methods: {
            filterUsers(data) {
                console.log(data);
            }
        },
        mounted: function () {
            $("#user_drop").dropdown({
                onChange: function (value) {
                    console.log(value);
                }
            })
        }
    }
</script>
