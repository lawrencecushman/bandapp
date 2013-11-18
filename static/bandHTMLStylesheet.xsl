<xsl:for-each select="Bands/Band">
    <xsl:value-of select="@name"/>
    <xsl:value-of select="Hometown/City/node()"/>,
    <xsl:value-of select="Hometown/StateOrProvince/node()"/>,
    <xsl:value-of select="Hometown/Country/node()"/>
    <xsl:for-each select="Genre">
        <xsl:value-of select="node()" />,
    </xsl:for-each>
    <xsl:for-each select="Performer">
        <xsl:value-of select="@instrument" />
        <xsl:value-of select="node()" />
        <xsl:value-of select="@join-date" />
    </xsl:for-each>

    <xsl:for-each select="Album">
    <xsl:value-of select="@title"/>
    <xsl:value-of select="ReleaseDate/node()"/>

        <xsl:for-each select="Song">
            <xsl:value-of select="@title"  />
            <xsl:value-of select="@length" />
        </xsl:for-each>
    </xsl:for-each>
</xsl:for-each>
