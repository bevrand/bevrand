<template>
    <div id="playlistCreationArea" class="playlistcreation">
        <navbar></navbar>
        <div id="creationArea" class="creationfield">
            <span class="label">
                <a class="image featured" ><img :src="imageUrl" ></a><br>
                <button v-on:click="setImage"> Change Image</button>
                <a class="playlistselector" id="playlistName"><h3> Playlist: {{ displayName }}</h3>  </a>
                <h3 style="margin-bottom: 0.5em">Beverages:</h3><br>
                <ul id="beverageList">
                    <li v-for="(beverage, index) in beverages" :key="index" >
                        {{ beverage }}
                        <a class="hover-edit">
                        <font-awesome-icon icon="pencil-alt" class="icons" v-on:click="editDrink(index)"/>
                        </a>
                        <a class="hover-delete">
                        <font-awesome-icon icon="trash" class="icons" v-on:click="removeDrink(index)" />
                        </a>
                    </li>
                </ul>
                </span>

            <div v-if="expandPopularDrinks">

                <button class="circledbutton"
                        v-for="(item, index) in popularDrinks"
                        :key="index"
                        style="background-color: orange"
                        v-on:click="() => setPopularDrink(item)">
                    <span>{{item}}</span>
                </button>

            </div>

            <a v-if="!expandPopularDrinks" class="hover-popular"><font-awesome-icon v-on:click="showPopularDrinks" icon="glass-martini" size="2x"/>
                <br>Show popular Drinks</a>

            <div>
                <input
                        v-model="drink"
                        placeholder="Drink you want to add"
                        type="text"
                        class="adddrink"
                        value=""
                />
                <a class="hover-add"><font-awesome-icon v-on:click="addBeverage()" icon="plus-circle" size="lg"/></a>
                <br>
                <button v-on:click="createNewPlaylist()"
                        v-if="beverages.length >= 2"
                        id="submitButton"
                        class="submitbutton">Save this playlist</button>
        </div>
        </div>
        <foot></foot>
    </div>
</template>


<script>
    import Footer from "../components/Footer.vue"
    import Navbar from "../components/Navbar.vue"

    export default {
        name: 'PlaylistCreation',
        data() {
            return {
                displayName: this.$route.params.displayName,
                beverages: [],
                drink: '',
                errors: [],
                normalizedPlayListName: '',
                username: this.$store.state.username,
                imageUrl: 'https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png',
                popularDrinks: ['Beer', 'Red Wine', 'White Wine', 'Vodka', 'Whiskey', 'Tequila'],
                expandPopularDrinks: false,
            };
        },
        mounted() {
            this.normalizeName();
        },
        created() {
        },

        components: {
            'navbar': Navbar,
            'foot': Footer,
        },
        methods: {
            normalizeName: function () {
                this.normalizedPlayListName = this.displayName.replace(/[^a-zA-Z0-9]/g, "")
                    .toLowerCase();
            },

            setImage() {
                this.$swal({
                    text: 'Enter an image url',
                    content: "input",
                    placeholder: "Image url",
                    buttons: {
                        cancel: true,
                        confirm: {
                            text: "Change!",
                            closeModal: true,
                        },
                    },
                })
                .then(value => {
                    if (value == null) {
                        this.$swal.stopLoading();
                        this.$swal.close()
                    }
                    else if (value.trim() === '') {
                        this.$swal('Value cannot be empty').then(() => {
                            this.setImage()
                        })
                    }
                    else {
                        this.$swal("Validation", "Changed image url", "success").then(() => {
                            this.imageUrl = value;
                        });
                    }
                })},
            addBeverage : function () {
                let normalizedDrink = this.drink.charAt(0).toUpperCase() + this.drink.slice(1);
                if (this.beverages.indexOf(normalizedDrink) > -1){
                    this.$swal('Selected drink is already in this playlist')
                }
                else if (normalizedDrink.length < 2 || normalizedDrink.trim() === '') {
                    this.$swal('Drink is too short or empty')
                }
                else {
                    this.beverages.push(normalizedDrink);
                    this.drink = ''
                }

            },
            removeDrink (index) {
                this.beverages.splice(index, 1)
                },
            editDrink (index) {
                this.$swal({
                    text: 'Enter a new name',
                    content: "input",
                    placeholder: "Beer",
                    buttons: {
                        cancel: true,
                        confirm: {
                            text: "Change",
                            closeModal: true,
                            },
                        },
                    })
                    .then(value => {
                        if (value == null) {
                            this.$swal.stopLoading();
                            this.$swal.close()
                        }
                        else if (value.trim() === '') {
                            this.$swal('Drink is too short or empty')
                        }
                        else {
                            this.drink = value;
                            this.addBeverage();
                            if(this.drink === '') {
                                this.$swal("Validation", `Changed ${this.beverages[index]} to ${value}`, "success");
                                this.removeDrink(index);
                            }
                        }
                    })},
            createNewPlaylist () {
                this.$apiClient({
                    method: "post",
                    url: `${this.$proxyUrl}/api/user`,
                    data: {
                        "beverages": this.beverages,
                        "displayName": this.displayName,
                        "imageUrl": this.imageUrl,
                        "list": this.normalizedPlayListName,
                        "user": "joeri"
                    }})
                    .then(response => {
                        this.$swal("Well done", `Playlist ${this.displayName} has been created`, "success").then(() => {
                            this.$router.push({ name: 'profilePage' });
                        });
                    })
                    .catch(e => {
                        this.$swal("Error", "Something went wrong", "error")
                    })
                },
                setPopularDrink (beverage) {
                    if (!this.beverages.indexOf(beverage) < 1) {
                        this.beverages.push(beverage);
                    }
                    this.expandPopularDrinks = !this.expandPopularDrinks;
                },

                showPopularDrinks () {
                    this.expandPopularDrinks = !this.expandPopularDrinks;
                }
            },
    };
</script>

<style scoped>
    .playlistcreation {
        background-color: #7A2F9E;
        text-align: center;
    }

    .image {
        position: relative;
        display: inline-block;
        border: 0;
        outline: 0;
    }

    .image img {
        display: block;
        width: 40%;
        height: 40%;
    }

    .image.featured {
        display: block;
        margin: 0 0 0 0;
        cursor: pointer;
    }

    ul {
        list-style-type: none;
    }

    .label {
        position: relative;
        top: 0;
        width: auto;
    }

    .label .image {
        position: relative;
        width: auto;
        margin-bottom: 1em;
    }

    .label h3 {
        margin-bottom: 1em;
        font-size: 1.5em;
        cursor: pointer;
        font-weight: bold;
        text-align: center;
    }

    .hover-add {
        margin-left: 1em;
    }

    .hover-add:hover {
        color: #68ff27;
    }

    .hover-popular {
        color: #ff9500;
    }

    .hover-delete {
        margin-left: 0.5em;
    }

    .hover-delete:hover {
        color: #ff271a;
    }

    .hover-edit {
        margin-left: 0.5em;
    }

    .hover-edit:hover {
        color: #3cfaff;
    }

    .adddrink {
        margin-bottom: 2em;
        font-family: "Ubuntu", sans-serif;
    }

    .circledbutton{
        position: relative;
        height: 3em;
        margin-left: 0.5em;
        margin-bottom: 0.5em;
        width: 9em;
        font-size:13px;
        font-family:arial, helvetica, sans-serif;
        padding: 10px 10px 10px 10px;
        text-shadow: -1px -1px 0 rgba(0,0,0,0.3);
        font-weight:bold;
        text-align: center;
        color: #FFFFFF;
        background-color: #FF9500;
    }

    .circledbutton:hover{
        background: #7A2F9E;
    }

    .submitbutton {
        position: relative;
        display: inline-block;
        background: #ff9500;
        color: #ffffff;
        text-align: center;
        border-radius: 0.5em;
        text-decoration: none;
        padding: 0.65em 3em 0.65em 3em;
        margin-top: 2em;
        margin-bottom: 2em;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
        font-size: 1em;
        font-family: "Ubuntu", sans-serif;
        -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out,
        color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
    }

    .submitbutton:hover {
        color: #fff;
        background: #424242;
        letter-spacing: 1px;
        -webkit-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        -moz-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        box-shadow: 5px 40px -10px rgba(0, 0, 0, 0.57);
        transition: all 0.4s ease 0s;
    }

</style>

