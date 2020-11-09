<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">  
		    <view class="top_view"></view>  
		</view>  
		<!-- #endif -->
		<view class="book_place">
			<text>读书广场</text>
		</view>
		<view class="book_place_rest">
			<view class="cu-bar" style="position: fixed;bottom:350upx;left: 550upx; width: 750upx;z-index: 9999;">
				<view @tap="gotalk()" class="action anniu">
					<view  class="action cuIcon-roundaddfill text-white anniu" style="font-size: 300%;color: black;">
			
					</view>
					
				</view>
			
			</view>
			<view class="rest_users">
				<view v-for="(item,index) in waim" :key="index" class="users_all">
					<view class="users_name">
						<image :src="item.wuserimage==null?'../../static/img/people_img.png':'item.wuserimage'"></image>
						<text style="text-align: center;font-weight: 700;color: blue;">{{item.wadminname}}</text>
						<view class="cu-tag bg-red radius" style="float: left;margin-top: 12upx; margin-left: 10upx;">管理员</view>
						
						
					</view>
					<view class="talk_book">
						<view class="talk_content">
							<view class="users_content" style="height: 70%;">
								<text>{{item.waimtitle}}</text>
							</view>
							<view class="gonggao_content" style="">
								<view class="" style="overflow: auto;">
									{{item.waimcontent}}
								</view>
								
							</view>
							<view style="display: flex; justify-content: space-between;">
								<view style="text-align: center;margin-top: 10upx;margin-left: 10upx;">
									<text>{{item.waimdate}}</text>
								</view>
							</view>
						</view>
					</view>
		
				</view>
		
		
			</view>
		</view>
		
		<view class="xidengbuttom">
		
		</view>
		<view class="book_place_rest">
			<view class="cu-bar" style="position: fixed;bottom:350upx;left: 550upx; width: 750upx;z-index: 9999;">
				<view @tap="gotalk()" class="action anniu">
					<view class="action cuIcon-roundaddfill text-white" style="font-size: 300%;color: black;">
			
					</view>
					
				</view>
			
			</view>
			<view class="rest_users">
				<view v-for="(item,index) in invitation" :key="index" class="users_all">
					<view class="users_name">
						<image :src="item.wuserimage==null?'../../static/img/people_img.png':'item.wuserimage'"></image>
						<text style="text-align: center;font-weight: 700;color: red;">{{item.wusername}}</text>
						<view class="cu-tag bg-red radius" style="float: left;margin-top: 12upx; margin-left: 10upx;">注册用户</view>
					</view>
					<view class="talk_book">
						<view class="talk_content">
							<view class="users_content" style="height: 70%;">
								<text>{{item.winvitate}}</text>
							</view>
							<view @tap="gotodetail(item.wbookid)" class="book_content">
								<image :src="item.wbookimage"></image>
								<text style="text-align: center;">{{item.winvitatebookname}}</text>
							</view>
							<view style="display: flex; justify-content: space-between;">
								<view style="text-align: center;margin-top: 10upx;margin-left: 10upx;">
									<text>{{item.winvitatedate}}</text>
								</view>
								<view class="cu-capsule radius" style="margin-bottom: 10upx;">
									<view class='cu-tag bg-grey '>
										<text class='cuIcon-likefill'></text>
									</view>
									<view class="cu-tag line-grey">
										{{item.winvitatestar}}
									</view>
								</view>
							</view>
						</view>
					</view>

				</view>


			</view>
		</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				text: 'uni-app',
				invitation: [],
				len_invitation: 0,
				b_limit:9,
				waim:[]

			}
		},
		onLoad() {
			this.getinvitation();
			this.get_waim();
			setTimeout(function() {
			}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success: function(res) { //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画

		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.getinvitation();
			this.get_waim();
		},
		onReady() {

		},
		methods: {
			gotalk(){
				var t_limit=0;
				var data ="";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					t_limit=data.walimit;
				} catch (e) {
					//TODO handle the exception
				};
				if(data!=""){
					uni.navigateTo({
					    url: "./talk",
						animationType:"slide-in-left",
						animationDuration:500
					});
				}else{
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.navigateTo({
								    url: "../login/login",
									animationType:"zoom-out",
									animationDuration:500
								});
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
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata-card?id=${id}`,
					animationType:"zoom-fade-out",
					animationDuration:500
				})
			},
			getinvitation() {
				var inv=""
				var invim=[]
				var data=""
				uni.request({
					url:  helper.baseUrl + "/card/invitate",
					data: {
					},
					success: (res) => {
						this.invitation = res.data.invatate;
						this.len_invitation = res.data.changdu;
						inv = JSON.stringify(res.data.invatate);
						uni.setStorage({
							key: "invim",
							data: inv,
							success() {},
							fail() {}
						});
						try {
							const res = uni.getStorageSync('invim');
							data = JSON.parse(res);
							this.invitation = data;
						} catch (e) {
							//TODO handle the exception
						};
					},
					fail: (res) => {
						try {
							const res = uni.getStorageSync('invim');
							data = JSON.parse(res);
							this.invitation = data;
						} catch (e) {
							//TODO handle the exception
						};
					}
				});
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					this.b_limit=data.walimit;
					} catch (e) {
						//TODO handle the exception
					};
					
				
			},
			get_waim() {
				var wim=""
				var wimim=[]
				var data=""
				uni.request({
					url: helper.baseUrl +"/card/adminim",
					data: {
					},
					success: (res) => {
						this.waim=res.data.data;
						wim = JSON.stringify(res.data.data);
						uni.setStorage({
							key: "wimim",
							data: wim,
							success() {},
							fail() {}
						});
						try {
							const res = uni.getStorageSync('wimim');
							data = JSON.parse(res);
							this.waim = data;
						} catch (e) {
							//TODO handle the exception
						};
					},
					fail: (res) => {
						try {
							const res = uni.getStorageSync('wimim');
							data = JSON.parse(res);
							this.waim = data;
						} catch (e) {
							//TODO handle the exception
						};
					}
				});
			},



		}
	}
</script>

<style>
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
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
	}

	.book_place_rest {
		padding-top: 5upx;
	}

	.rest_users {

		padding-bottom: 5upx;
	}

	.users_name {
		height: 70upx;
		line-height: 70upx;
		display: flex;
		padding: 5upx 5upx;
		/* border-bottom: 1px solid #e4e4e4; */
	}

	.users_name image {
		width: 60upx;
		height: 60upx;
		margin: 0 10upx;

	}
	.gonggao_content {
		display: flex;
		background: #E5e5e5;
		border-radius: 7px;
		margin: 10upx 10upx;
		margin-bottom: 10upx;
		padding: 10upx 10upx;
		/* border: 1px solid #e4e4e4; */
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

	.users_all {
		border: 1px solid #e0e0e0;
		margin-bottom: 5upx;

	}

	.users_content {
		margin: 10upx 10upx;
	}
	.anniu{
		width: 40upx;
		height: 40upx;
		padding: 8upx 8upx;
		border-radius: 50upx;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: rgba(41,36,33,0.2);
	}
	.xiding {
		width: 100%;
		height: var(--status-bar-height);
	}
	
	.xidengbuttom {
		height: calc(100upx + env(safe-area-inset-bottom) / 2);
		width: 100%;
		min-height: 100upx;
	}
</style>
