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
				<text>留言反馈</text>
			</view>
		</view>
		<view>
			<view class="cu-bar bg-white solid-bottom margin-top" style="margin-bottom: 10upx;">
				<view class="action">
					<text class="cuIcon-title text-orange "></text>反馈列表
				</view>
			</view>
			<view class="cu-list menu-avatar">
				<view v-for="(item,index) in message_list" :key="item" class="cu-item">
					<view class="cu-avatar round lg" style="background-image: url(../../static/img/shequ.png);"></view>
					<view class="content">
						<view class="text-grey">
							<view class="cu-tag round sm" style="margin-left: 20upx;font-weight: 400;font-size: 20upx;">
								反馈用户id:{{item.wuserid}}
							</view>
							<view class="cu-tag round sm" style="margin-left: 20upx;font-weight: 400;font-size: 20upx;">
								反馈标题:{{item.wumessagetitle}}
							</view>
						</view>
						<view class="text-gray text-sm flex">
							<view class="text-cut">
								<text class="text-red margin-right-xs"></text>
								反馈内容:{{item.wumessagecontent}}
							</view>
						</view>
					</view>
					<view class="action">
						<view class="cu-tag round bg-grey sm">反馈时间</view>
						<view class="text-grey text-xs">{{item.winserttime}}</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				message_list:"",
				mylists: {
					name: "my",
					url: "../my/my",
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
						url:"./admin"
					})
				}
				
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
			
		},
		onLoad() {
			this.get_message();
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
