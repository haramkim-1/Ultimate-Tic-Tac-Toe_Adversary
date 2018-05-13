package com.theaigames.engine.io;

import java.io.IOException;

public interface Bot {
    /**
     * Write a string to the bot
     * @param line : input string
     * @throws IOException
     */
    public void writeToBot(String line) throws IOException;

    /**
     * Wait's until the this.response has a value and then returns that value
     * @param timeOut : time before timeout
     * @return : bot's response, returns and empty string when there is no response
     */
    public String getResponse(long timeOut);

    /**
     * Add a warning to the bot's dump that the engine outputs
     * @param warning : the warning message
     */
    public void outputEngineWarning(String warning);

}
