# frozen_string_literal: true

class DecisionsController < ApplicationController
  def index
    @decisions = Decision.all.order(date: :desc, created_at: :desc)
  end

  def show; end

  def new; end

  def create; end

  def edit; end

  def update; end

  def destroy; end
end
