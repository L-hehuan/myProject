<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="userim-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				我的主页
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text >个人信息</text>
			</view>
			
		</view>
		<!-- <view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
			<view class="cu-item ">
				<view class="content flex justify-center align-center">
					<text class="text-black" style="font-weight: bold;"><b>我的信息</b></text>
					<text class="text-grey"></text>
				</view>
			</view>
		</view> -->
		<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
			<view class="" style="padding-bottom: 10upx;">
				我的基本信息
			</view>
			<view @tap="changeim(useri.wuserimage)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>头像: </b></text>
					<image :src="useri.wuserimage==null?'../../static/img/people_img.png':useri.wuserimage" style="float: right;" ></image>
				</view>

				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeim(useri.wusername)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>用户名: </b></text>
					<text  style="float: right;" class="text-grey">{{useri.wusername}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeim(useri.wuserid)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>用户id: </b></text>
					<text style="float: right;" class="text-grey">{{useri.wuserid}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeim(useri.wuserphone)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>手机号: </b></text>
					<text  style="float: right;" class="text-grey">{{useri.wuserphone}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeim(useri.wuserinsert_time)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>注册时间: </b></text>
					<text style="float: right;" class="text-grey">{{useri.wuserinsert_time}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeim(useri.walimit)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>用户权限: </b></text>
					<text style="float: right;" class="text-grey" >{{useri.walimit==9?'个人用户':'会员用户'}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<!-- <view  @tap="gochangeuser()" style="width: 300upx;margin-left: 200upx;" class="change-user cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
				<view class="cu-item ">
					<view class="content flex justify-center align-center">
						<text class="text-black" style="color: red;">修改个人信息</text>
						<text class="text-grey"></text>
					</view>
				</view>
			</view> -->
		</view>
		<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
			<view class="" style="padding-bottom: 10upx;">
				账号绑定与关联
			</view>
			<view @tap="bindwp()" class="cu-item ">
				<view class="content">
					<image src="../../static/img/phoenyanz.png"></image>
					<text class="text-black"><b>手机号: </b></text>
					<text style="float: right;" class="text-grey">{{useri!=""?(useri.walimit==9?'未验证':useri.wuserphone):'未验证'}}</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="bindqq()" class="cu-item ">
				<view class="content">
					<image src="../../static/img/QQ.png"></image>
					<text class="text-black"><b>QQ </b></text>
					<text style="float: right;" class="text-grey">未绑定</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="bindwx()" class="cu-item ">
				<view class="content">
					<image src="../../static/img/weinxinz.png"></image>
					<text class="text-black"><b>微信 </b></text>
					<text style="float: right;" class="text-grey">未绑定</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
		</view>
		<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
			<view class="" style="padding-bottom: 10upx;">
				账号与密码
			</view>
			<view @tap="changepas(useri.wuserid)" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>登录密码 </b></text>
					<text style="float: right;" class="text-grey">修改密码</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
			<view @tap="changeup()" class="cu-item ">
				<view class="content">
					<text class="text-black"><b>登陆手机号 </b></text>
					<text style="float: right;" class="text-grey">修改</text>
				</view>
				<view class="" style="padding-left: 10upx;">
					<text class="cuIcon-right"></text>
				</view>
			</view>
		</view>


	</view>
</template>

<script>
	import helper from "../../common/until.js"
	export default {
		data() {
			return {
				useri: ""

			}
		},
		onLoad() {
			this.getmy();
		},
		methods: {
			changepas(id){
				var data = "";
				var user_login=[];
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "/user/gerenxinxi",
						data: {
							userid: data.wuserid
						},
						method: "POST",
						success: (res) => {
							this.useri = res.data.data;
							user_login = JSON.stringify(res.data.data);
							uni.setStorage({
								key: "userim",
								data: user_login,
								success() {},
								fail() {}
							});
						},
						fail: (res) => {
							this.useri=data;
						}
					})
				} else {
					uni.showToast({
						icon: "none",
						title: "请先进行登录"
					})
				}
				if(this.useri.walimit==9){
					uni.showToast({
						icon:"none",
						title:"请先验证手机号"
					})
				}else{
					uni.navigateTo({
						url:`./impas?id=${id}`,
						animationType:"slide-in-left",
						animationDuration:400
					})
				}
				
				
			},
			gomy() {
				var url = "../my/my";
				if (url != null && url != undefined) {
					uni.switchTab({
						url:url
					});
				}

			},
			changeup(){
				uni.showToast({
					icon:"none",
					title:"暂未开放"
				})
			},
			changeim(strname){
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if(strname==data.wuserimage){
					uni.showToast({
						icon:"none",
						title:"暂不支持更换头像"
					})
				}else if(strname==data.wusername){
					uni.navigateTo({
						url:`./imname?id=${data.wuserid}`,
						animationType:"slide-in-left",
						animationDuration:400
					})
				}else if(strname==data.wuserphone){
					if(data.walimit==9){
						uni.showToast({
							icon:"none",
							title:"请先对手机号进行验证"
						})
					}else{
						uni.showToast({
							icon:"none",
							title:"您的手机号验证已通过"
						})
					}
				}else if(strname==data.wuserinsert_time){
					uni.showToast({
						icon:"none",
						title:"注册时间不支持修改"
					})
				}else if(strname==data.wuserid){
						uni.showToast({
							icon:"none",
							title:"用户ID不支持更改"
						})
				}else if(strname==data.walimit){
					if(strname==9){
						uni.showToast({
							icon:"none",
							title:"您的用户等级为V0"
						})
					}else{
						uni.showToast({
							icon:"none",
							title:"您的用户等级为V1"
						})
					}
				}else{
					uni.showToast({
						icon:"none",
						title:"未知错误,请联系管理员"
					})
				}
			},
			bindwp(){
				if(this.useri.walimit==9){
						uni.navigateTo({
							url:"./rmphone",
							animationType:"slide-in-left",
							animationDuration:400
						})
				}else if(this.useri.walimit==99){
					uni.showToast({
						icon:"success",
						title:"手机号已验证"
					})
				}
				
			},
			bindqq(){
				uni.showToast({
					icon:"none",
					title:"暂未开放"
				})
			},
			bindwx(){
				uni.showToast({
					icon:"none",
					title:"暂未开放"
				})
			},
			getmy() {
				var data = "";
				var user_login=[];
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "/user/gerenxinxi",
						data: {
							userid: data.wuserid
						},
						method: "POST",
						success: (res) => {
							user_login = JSON.stringify(res.data.data);
							uni.setStorage({
								key: "userim",
								data: user_login,
								success() {},
								fail() {}
							});
							this.useri = res.data.data;
						},
						fail: (res) => {
							this.useri=data;
						}
					})
				} else {
					uni.showToast({
						icon: "none",
						title: "请先进行登录"
					})
				}
			},
			gochangeuser() {
				var url = "./userchange";
				if (url != null && url != undefined) {
					uni.navigateTo({
					    url: url,
						animationType:"slide-in-left",
						animationDuration:500
					});

				}
			}

		}
	}
</script>

<style>
	.change-user:hover{
		background-color: #333333;
	}
	.userim-top{
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 120upx;
	}
	.status_bar {
		height: var(--status-bar-height);
		width: 100%;
		background-color: #F8F8F8;
	}

	.top_view {
		height: var(--status-bar-height);
		width: 100%;
		position: fixed;
		background-color: #F8F8F8;
		top: 0;
		z-index: 999;
	}
</style>
