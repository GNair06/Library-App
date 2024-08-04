export default{
    data(){
        return{
            user: null,
            flag: false
        };
    },
    async created(){
        await this.loggedin();
    },
    methods:{
        async loggedin(){
            const access_token = localStorage.getItem('access_token');
            if(!access_token){
                this.flag == false;
                return;
            }
            try{
                this.user = await this.user_data(access_token);
                this.role = this.user.role;
                this.id = this.user.id;
                this.name = this.user.name;
                this.flag = true;
            }
            catch(error){
                console.error('Error:', error);
                this.flag = false
            }
        },
        async user_data(access_token){
            const response = await fetch('http://localhost:5000/get_user_data',{
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${access_token}`
                }
            });
            if (response.status === 401){
                this.flag = false;
                return null;
            }
            return await response.json();
        },
        async logout(){
            fetch('http://localhost:5000/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            })
            .then(() => {
                localStorage.removeItem('access_token');
                this.user = null;
                this.flag = false;
                this.$router.push('/login')
            })
            .catch(error => {
                console.log("Error:", error);
            })
        }
    }
}