/*
 * Copyright 2016 riddles.io (developers@riddles.io)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 *
 *     For the full copyright and license information, please view the LICENSE
 *     file that was distributed with this source code.
 */

package com.theaigames.game.player;

import java.io.IOException;

import com.theaigames.engine.io.IOPlayer;

/**
 * AbstractPlayer class
 * 
 * DO NOT EDIT THIS FILE.
 * 
 * Extend this abstract class to store information about the player, to get 
 * bot responses and to send the bot information.
 * Extra methods and variables can be added to handle game specific stuff.
 * 
 * @author Jim van Eeden <jim@starapple.nl>
 */

public abstract class AbstractPlayer {
	
	private String name;
	private IOPlayer bot;
	private long timeBank;
	private long maxTimeBank;
	private long timePerMove;
	
	public AbstractPlayer(String name, IOPlayer bot, long maxTimeBank, long timePerMove) {
		this.name = name;
		this.bot = bot;
		this.timeBank = maxTimeBank;
		this.maxTimeBank = maxTimeBank;
		this.timePerMove = timePerMove;
	}
	
	/**
	 * @return : The String name of this Player
	 */
	public String getName() {
		return name;
	}
	
	/**
	 * @return : The time left in this player's time bank
	 */
	public long getTimeBank() {
		return timeBank;
	}
	
	/**
	 * @return : The Bot object of this Player
	 */
	public IOPlayer getBot() {
		return bot;
	}

	/**
	 * Sets the time bank directly
	 */
	public void setTimeBank(long time) {
		this.timeBank = time;
	}
	
	/**
	 * Updates the time bank for this player, cannot get bigger than maximal time bank or smaller than zero
	 * @param timeElapsed : time consumed from the time bank
	 */
	public void updateTimeBank(long timeElapsed) {
		this.timeBank = Math.max(this.timeBank - timeElapsed, 0);
		this.timeBank = Math.min(this.timeBank + this.timePerMove, this.maxTimeBank);
	}
	
	/**
	 * Send one setting to the player
	 * @param type : setting type
	 * @param value : setting value
	 */
	public void sendSetting(String type, String value) {
		sendLine(String.format("settings %s %s", type, value));
	}
	
	/**
	 * Send one setting to the player
	 * @param type : setting type
	 * @param value : setting value
	 */
	public void sendSetting(String type, int value) {
		sendLine(String.format("settings %s %d", type, value));
	}
	
	/**
	 * Sends one update to the player about another player or himself
	 * @param type : type of update
	 * @param player : what player the update is about
	 * @param value : value of the update
	 */
	public void sendUpdate(String type, AbstractPlayer player, String value) {
		sendLine(String.format("update %s %s %s", player.getName(), type, value));
	}
	
	/**
	 * Sends one update to the player about another player or himself
	 * @param type : type of update
	 * @param player : what player the update is about
	 * @param value : value of the update
	 */
	public void sendUpdate(String type, AbstractPlayer player, int value) {
		sendLine(String.format("update %s %s %d", player.getName(), type, value));
	}
	
	/**
	 * Sends one update to the player about the game in general, like round number
	 * @param type
	 * @param value
	 */
	public void sendUpdate(String type, String value) {
		sendLine(String.format("update game %s %s", type, value));
	}
	
	/**
	 * Sends one update to the player about the game in general, like round number
	 * @param type : type of update
	 * @param value : value of the update
	 */
	public void sendUpdate(String type, int value) {
		sendLine(String.format("update game %s %d", type, value));
	}
	
	/**
	 * Asks the bot for given move type and returns the answer
	 * @param moveType : type of move the bot has to return
	 * @return : the bot's output
	 */
	public String requestMove(String moveType) {
		long startTime = System.currentTimeMillis();
		
		// write the request to the bot
		sendLine(String.format("action %s %d", moveType, this.timeBank));

		// wait for the bot to return his response
		String response = this.bot.getResponse(this.timeBank);
		
		// update the timebank
		long timeElapsed = System.currentTimeMillis() - startTime;
		updateTimeBank(timeElapsed);
		
		return response;
	}
	
	/**
	 * Sends given string to bot
	 * @param info
	 */
	private void sendLine(String content) {
		try {
			this.bot.writeToBot(content);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
