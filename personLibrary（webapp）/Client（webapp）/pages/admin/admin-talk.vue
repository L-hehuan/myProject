<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="zhuce-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				返回
			</view>
			<view class="book_place">
				<text>发布公告</text>
			</view>
		</view>
		<view class="cu-form-group margin-top">
			<view class="title">公告标题</view>
			<input type="text" placeholder="不超过八个字" value="" v-model="form.title"/>
		</view>
		<view class="cu-form-group align-start">
			<view class="title">公告栏</view>
			<textarea v-model="form.content" maxlength="-1" :disabled="modalName!=null" input="" placeholder="请输入发布的公告消息"></textarea>
		</view>
		<view class="flex justify-center" style="margin-top: 40upx;">
			<button @tap="tijiao()" class="bg-gradual-red round" style="width: 650upx;">
				发布公告
			</button>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				index: -1,
				modalName: null,
				form:{
					title:"",
					content:"",
					username:""
				}
			}
		},
		methods: {
			gomy(){
				var data=""
				try{
					const res=uni.getStorageSync("adminim");
					data =JSON.parse(res);
				} catch(e){
					
				}
				if(data==""){
					uni.showToast({
						icon:"none",
						title:"系统繁忙"
					})
					uni.reLaunch({
						url:"../login/admin-login"
					})
				}else{
					uni.reLaunch({
						url:"./gongao_manage"
					})
				}
				
			},
			tijiao(){
				var data="";
				var fu_name="";
				if(this.form.title=="" || this.form.content==""){
						uni.showToast({
							icon:"none",
							title:"请检查你的输入是否有空项"
						})
				}else{
					try {
						const res = uni.getStorageSync('adminim');
						data = JSON.parse(res);
						this.form.username = data.wadminname;
						
					} catch (e) {
						//TODO handle the exception
					};
					uni.request({
						url:helper.baseUrl+"/card/imformation",
						data:{
							title:this.form.title,
							name:this.form.username,
							content:this.form.content
						},
						method:"POST",
						success: (res) => {
							uni.showToast({
								icon:"none",
								title:res.data.desc,
								duration:5000
							})
							uni.reLaunch({
								url:"./gongao_manage"
							})
						},
						fail: (res) => {
							uni.showToast({
								icon:"none",
								title:"网络连接失败"
							})
						},
					})
					
				}
				
			},
		}
	}
</script>

<style>
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 200upx;
	}
	.zhuce-top {
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
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
