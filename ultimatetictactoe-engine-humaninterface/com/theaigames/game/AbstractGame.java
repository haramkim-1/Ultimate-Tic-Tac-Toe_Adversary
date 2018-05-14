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

package com.theaigames.game;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.theaigames.engine.Engine;
import com.theaigames.engine.Logic;
import com.theaigames.engine.io.Bot;
import com.theaigames.engine.io.IOPlayer;
import com.theaigames.game.player.AbstractPlayer;

/**
 * abstract class AbstractGame
 * 
 * DO NOT EDIT THIS FILE
 * 
 * Extend this class with your main method. In the main method, create an
 * instance of your Logic and run setupEngine() and runEngine()
 * 
 * @author Jim van Eeden <jim@starapple.nl>
 */

public abstract class AbstractGame implements Logic {
	
	public Engine engine;
	public GameHandler processor;
	
	public int maxRounds;
	public int botId;
	
	public boolean DEV_MODE = false; // turn this on for local testing
	public String TEST_BOT; // command for the test bot in DEV_MODE
	public int NUM_TEST_BOTS; // number of bots for this game
	protected boolean LOG_MOVES = false; // whether game/player messages should be logged. Modification.
	
	public AbstractGame() {
		maxRounds = -1; // set this later if there is a maximum amount of rounds for this game
	}

	/**
	 * Partially sets up the engine
	 * @param args : command line arguments passed on running of application
	 * @throws IOException
	 * @throws RuntimeException
	 */
	public void setupEngine(String args[]) throws IOException, RuntimeException {
		
        // create engine
        this.engine = new Engine();
        
        // add the test bots if in DEV_MODE
        if (DEV_MODE) {
            if (TEST_BOT.isEmpty()) {
                throw new RuntimeException("DEV_MODE: Please provide a command to start the test bot by setting 'TEST_BOT' in your main class.");
            }
            if (NUM_TEST_BOTS <= 0) {
                throw new RuntimeException("DEV_MODE: Please provide the number of bots in this game by setting 'NUM_TEST_BOTS' in your main class.");
            }
            
            for (int i = 0; i < NUM_TEST_BOTS; i++) {
                this.engine.addPlayer(TEST_BOT, "ID_" + i, LOG_MOVES);
            }
            
            return;
        }

		if (args.length <= 0) {
			throw new RuntimeException("No arguments provided.");
		} else if (args.length != 2) {
			throw new RuntimeException("Incorrect number of arguments provided.");
		}

		try {
			botId = Integer.parseInt(args[0]);
			if (botId != 1 && botId != 2) {
				throw new RuntimeException("Argument 1 is not 1 or 2.");
			}

			//add players
			if (botId == 2)
				this.engine.addHumanPlayer("1", LOG_MOVES);
			this.engine.addPlayer(args[1], botId + "", LOG_MOVES);
			if (botId == 1)
				this.engine.addHumanPlayer("2", LOG_MOVES);

		} catch (NumberFormatException e) {
			throw new RuntimeException("Argument 1 is not an integer.");
		}
	}
	
	/**
	 * Implement this class. Set logic in the engine and start it to run the game
	 */
	protected abstract void runEngine() throws Exception;
	
	/**
	 * @return : True when the game is over
	 */
	@Override
	public boolean isGameOver()
	{
		return this.processor.isGameOver()
				|| (this.maxRounds >= 0 && this.processor.getRoundNumber() > this.maxRounds);
	}
	
	/**
	 * Play one round of the game
	 * @param roundNumber : round number
	 */
	@Override
    public void playRound(int roundNumber) 
	{
		for(Bot player : this.engine.getPlayers()) {
			if (player instanceof IOPlayer)
				((IOPlayer) player).addToDump(String.format("Round %d", roundNumber));
		}
		
		this.processor.playRound(roundNumber);
	}
	
	/**
	 * close the bot processes, save, exit program
	 */
	@Override
	public void finish() throws Exception
	{
		// stop the bots
		for (Bot p : this.engine.getPlayers()) {
			if (p instanceof IOPlayer)
				((IOPlayer) p).finish();
		}
		Thread.sleep(100);
		
		if (DEV_MODE) { // print the game file when in DEV_MODE
			String playedGame = this.processor.getPlayedGame();
			System.out.println(playedGame);
		} else { // save the game to database
			try {
				this.saveGame();
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
		
		System.out.println("Done.");
		
        System.exit(0);
	}
	
	/**
	 * Does everything that is needed to store the output of a game
	 */
	public void saveGame() {
		AbstractPlayer winner = this.processor.getWinner();
		if (winner == null)
			System.out.println("Draw!");
		else
			System.out.println("winner: " + this.processor.getWinner().getName());

		// save results to file here
		String playedGame = this.processor.getPlayedGame();
		System.out.println(playedGame);
	}
}
