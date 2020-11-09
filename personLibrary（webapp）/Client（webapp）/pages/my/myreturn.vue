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
				<text >我的发布</text>
			</view>
			
		</view>
		<view>
			<view class="cu-bar bg-white solid-bottom margin-top" style="margin-bottom: 10upx;">
				<view class="action">
					<text class="cuIcon-title text-orange "></text>我发布的贴子
				</view>
			</view>
		</view>
		<view class="cu-item shadow">
			
		
			<view v-for="(item,index) in message_list.data" :key="index" class="cu-list menu-avatar comment solids-top ">
				<view class="cu-item">
					<view class="cu-avatar round users_name">
						<image :src="item.wuserimage==null?'../../static/img/people_img.png':'item.wuserimage'"></image>
					</view>
					<view class="content">
						<view class="text-grey">{{item.wusername}}</view>
						<view class="text-gray text-content text-df">
							{{item.winvitate}}
						</view>
						<view class="bg-white padding-sm radius margin-top-sm  text-sm">
							<view class="flex book_content">
								<image :src="item.wbookimage"></image>
								<text style="text-align: center;">{{item.winvitatebookname}}</text>
							</view>
						</view>
						<view class="margin-top-sm flex justify-between">
							<view class="text-gray text-df">{{item.winvitatedate}}</view>
							<button @tap="godelete(item.winvitateid)" style="margin-bottom: 5upx;" class="cu-btn bg-grey ">删除</button>
						</view>
					</view>
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
				message_list: ""
			}
		},
		onLoad() {
			this.gettiezi();
			setTimeout(function() {
				// console.log('start pulldown');
			}, 1000);
			uni.startPullDownRefresh({
				success: function(res) {
					// console.log(res); //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画
		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			// console.log('refresh');
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.gettiezi();
		},
		methods: {
			gettiezi() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl+"/my/wodeshoucang",
						data: {
							username: data.wusername
						},
						method: "POST",
						success: (res) => {
							this.message_list = res.data;
						}
					})
				} else if (data == "") {
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.reLaunch({
									url: "../login/login"
								})
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "取消登录"
								})
							}
						}
					});
				}
			},
			gomy() {
				var url = "./my";
				if (url != null && url != undefined) {
					uni.reLaunch({
						url: url
					});
				}
			
			},
			godelete(iid){
				var data="";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				}
				uni.showModal({
					title: '提示',
					content: '是否删除?',
					success: function(res) {
						if (res.confirm == true) {
							uni.request({
								url:helper.baseUrl+"/my/remove_favious",
								data:{
									iid:iid,
									username:data.wusername
								},
								method:"POST",
								success: (res) => {
									if(res.data.status==0){
										uni.showToast({
											icon:"success",
											title:res.data.desc
										})
										uni.reLaunch({
											url:"./my"
										})
									}else if(res.data.status==1){
										uni.showToast({
											icon:"none",
											title:res.data.desc
										})
									}
								}
							})
						} else if (res.cancel == true) {
							uni.showToast({
								icon: "none",
								title: "取消操作"
							})
						}
					}
				});
			}
		}
	}
</script>

<style>
	.users_name image {
		width: 60upx;
		height: 60upx;
	
	}
	
	.book_content {
		height: 100upx;
		line-height: 80upx;
		display: flex;
		background: #E5e5e5;
		border-radius: 7px;
		margin: 10upx 10upx;
		margin-bottom: 10upx;
		padding: 10upx 10upx;
		/* border: 1px solid #e4e4e4; */
	}
	
	.book_content image {
		width: 80upx;
		height: 80upx;
		/* background: #E5e5e5; */
		margin: 0 20upx;
	
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

</style>
