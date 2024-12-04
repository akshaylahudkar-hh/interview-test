# frozen_string_literal: true

module Api
  class HelloController < ApplicationController
    def index
      puts 'HELLO'
      render json: { hello: 'world' }
    end
  end
end
