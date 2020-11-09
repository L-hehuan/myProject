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
				<text>用户管理</text>
			</view>
		</view>
		<view style="" class="user-admin">
			<view v-for="(p,i) in userim" :key="i" class="user-im-admin">
				<view style="width: 120upx;height: 200upx;" class="">
					<image style="width: 100upx;height: 100upx;margin-top: 10upx;margin-left: 10upx;" :src="userim.wuserimage==null?'../../static/img/people_img.png':userim.wuserimage"></image>
					<view style="width: 120upx;height: 80upx;"  class=""></view>
				</view>
				<view class="" style="width: 390upx;height: 200upx;">
					<view class="" style="height: 50upx;width: 390upx;line-height: 50upx;">
						<text style="margin-right: 10upx;">用户名:</text>
						{{p.wusername}}
					</view>
					<view class="" style="height: 50upx;width: 390upx;line-height: 50upx;">
						<text style="margin-right: 10upx;">用户ID:</text>{{p.wuserid}}
					</view>
					<view class="" style="height: 50upx;width: 390upx;line-height: 50upx;">
						<text style="margin-right: 10upx;">用户手机号:</text>{{p.wuserphone}}
					</view>
					<view class="" style="height: 50upx;width: 390upx;line-height: 50upx;">
						<text style="margin-right: 10upx;">注册时间:</text>{{p.wuserinsert_time}}
					</view>
				</view>
				<!-- <view class="" style="height: 200upx;width: 230upx;">
					<view class="flex flex-wrap" style="height: 200upx;width: 100%;">
						<view class="" style="height: 100%;width: 50%;text-align: center;line-height: 200upx;">
							反馈消息
						</view>
						<view class="" style="height: 185upx;width: 50%;margin-top: 5upx;">
							<view class="" style="width: 100%;height: 50%;line-height: 95upx;background: #FF0000;border-radius: 5px;margin-bottom: 5upx;">
								<text style="font-size: 12upx;padding-left: 5upx;padding-right: 5upx;">未处理:</text>
							</view>
							<view class="" style="width: 100%;height: 50%;line-height: 95upx;border-radius: 5px;background:#F0AD4E">
								<text style="font-size: 12upx;padding-left: 5upx;padding-right: 5upx;">已处理:</text>
							</view>
						</view>
					</view>
					
				</view> -->
			</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				userim:"",
				message_list:"",
				message:"",
				message_se:""
			}
		},
		onLoad() {
			this.get_user();
			this.get_message();
		},
		methods: {
			get_user() {
				uni.request({
					url: helper.baseUrl+"/admin/seeuser",
					data: {
			
					},
					success: (res) => {
						this.userim=res.data.data;
					}
				})
			},
			get_message() {
				uni.request({
					url: helper.baseUrl+"/admin/seemessage",
					data: {
			
					},
					success: (res) => {
						this.message_list=res.data.data;
						
					}
				})
			},
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
						url:"./admin"
					})
				}
				
			}
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
	.user-im-admin{
		display: flex;
		background: #FFFFFF;
		width: 100%;
		height: 200upx;
		margin-bottom: 10upx;
	}
	.user-admin{
		margin-top: 20upx;
		margin-bottom:20upx ;
	}

</style>
