# frozen_string_literal: true

class DecisionsController < ApplicationController
  def index
    @decisions = Decision.all.order(date: :desc, created_at: :desc)
  end

  def show
    @decision = Decision.find(params[:id])
  end

  def new
    @decision = Decision.build(status: :pending, date: Time.zone.today)
  end

  def create
    @decision = Decision.new(decision_params)

    if @decision.save
      redirect_to @decision
    else
      render "new"
    end
  end

  def edit
    @decision = Decision.find(params[:id])
  end

  def update
    @decision = Decision.find(params[:id])

    if @decision.update(decision_params)
      redirect_to @decision
    else
      render :edit, status: :bad_request
    end
  end

  def destroy; end

  def decision_params
    params.require(:decision).permit(:title, :date, :description, :status)
  end
end
