class SignUpsController < ApplicationController
  allow_unauthenticated_access

  def show
    @user = User.new
  end

  def create
    @user = User.new(sign_up_params)
    if @user.save
      start_new_session_for(@user)
      redirect_to root_path
    else
      render :show, status: :unprocessable_entity
    end
  end

  private

  def sign_up_params
    sign_up_params = params.expect(user: %i[first_name last_name email_address password password_confirmation])
    sign_up_params[:display_name] = "#{sign_up_params[:first_name]} #{sign_up_params[:last_name]}"
    sign_up_params
  end
end
